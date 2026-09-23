"""C237: passive signal-path audit of frozen C236 models; no ability gate."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import unittest

import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C237-v5b-frozen-binding-signal-audit"
STAGE = "V5-B-FROZEN-BINDING-SIGNAL-AUDIT"
BASE = "eb2d5ed3cf6504b98152246f9583239427ea0fbc"
PARENT_EXECUTION = "0bc91722ca27803f065d2458505b502a2d01e50f"
PARENT_SHA = "0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec"
PARENT_ARTIFACTS = {
    "measurements.json": "19d24911d53e08898324514fedaafc32f27168f1526f9958b1572481cf957971",
    "probe-dataset.json": "bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c",
    "probe-plan.json": "86f534a54964a31d0139d5a3ceb3ef4b5e3c2ab46667adb002390a5b5d347957",
    "trained-models.pt": "90c711f1609b77d426395446e9e7757b2a897c6e2372322fabe3c16cf5f6fc45",
    "validation-summary.json": "a1e46ad4b0373daf6c1a920edc1ec8b7be5f9ab7f6c56490a9baa89062232042",
}
SEEDS, FAMILIES = (234001, 234002, 234003), ("full", "gru_only")
VIEWS = ("normal", "evidence_blind", "query_blind")
LAYERS = ("gru_eos", "pooled", "readout", "logits")
PAIR_KINDS = ("query", "facts", "order")
PAD, BOS, EOS, TOL = 256, 257, 258, 1e-9
OWN = (
    "fold_lm/v05_benchmarks/model_c237_frozen_signal_audit.py",
    "tests_lm/test_v05_c237_frozen_signal_audit.py",
    "tools/run_c237.ps1", "tools/invoke_c237.ps1",
    "docs/experiment-ledger-addendum-c237-preregistration.md",
    "docs/v5b-frozen-binding-signal-audit-v0.1.md",
)
OUTPUTS = {"diagnostic-plan.json", "traces.json", "contrasts.json", "diagnostics.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "1e5ab23f80a3cf2b510ce82bdd9f343b53716a6dc9641eb9b09ae6dd165c06ce"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c236_minimal_binding as parent
    return parent


def context():
    parent = parent_module()
    _, binding, factory, audit = parent.context()
    return parent, binding, factory, audit


def identities():
    return list(itertools.product(SEEDS, FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        identities=[list(x) for x in identities()], frozen="all six C236 step400 states; final_sha256",
        cohort_rows=16, languages=["en", "ja"], views=list(VIEWS), layers=list(LAYERS),
        pair_kinds=list(PAIR_KINDS), pairs_per_kind_per_language=4, paired_contrasts=144,
        masked_row_contrasts=192, diagnostic_cells=12, model_forward_calls=36,
        row_presentations=576, decoder_reconstructions=18, new_training_steps=0,
        optimizer_steps=0, checkpoint_writes=0, network_calls=0,
        capture="passive GRU output at actual EOS; norm input/output; decoder input; model logits",
        comparison="three plain forwards then three captured forwards per frozen model",
        difference="exact tensor equality plus raw linf/l2/relative_l2; no ability cutoff",
        output_measurement="unconstrained256-byte argmax; signed logit(1)-logit(0); top-two gap",
        integrity_tolerance=TOL, dtype="float64", device="cpu", threads=2,
        deterministic_algorithms=True, source_pins=268, protected_inputs=394,
        direct_dependencies=13, own_tests=24, modules=122, loaded_tests=2858, focused_tests=2857,
        excluded_test=EXCLUDED, gate="integrity only; no accuracy or sensitivity success threshold",
        general_language_claim=False, causal_claim=False, gate_f_candidate=False)


def eos_indices(tokens):
    require(tokens.dtype == torch.int64 and tokens.ndim == 2 and tokens.shape == (16,48), "token shape")
    require(bool(((tokens >= 0) & (tokens <= EOS)).all()), "token range")
    valid = tokens != PAD
    indices = valid.sum(1)-1
    positions = torch.arange(48, device=tokens.device)[None,:]
    require(bool((valid == (positions <= indices[:,None])).all()), "noncontiguous prefix")
    require(bool((tokens[:,0] == BOS).all()) and bool(((tokens == BOS).sum(1) == 1).all())
        and bool(((tokens == EOS).sum(1) == 1).all())
        and bool((tokens[torch.arange(16, device=tokens.device),indices] == EOS).all()), "BOS/EOS structure")
    return indices


def finite_tensor(value, shape):
    require(isinstance(value, torch.Tensor) and value.shape == shape and value.dtype == torch.float64
        and value.device.type == "cpu" and bool(torch.isfinite(value).all()), "capture shape/dtype/nonfinite")
    return value


def prediction_record(logits):
    require(len(logits) == 3, "view count")
    return {mode:finite_tensor(x,(16,256)).argmax(-1).tolist() for mode,x in zip(VIEWS,logits,strict=True)}


def metric_error(actual, expected):
    require(set(actual) == set(expected) == {"en","ja"}, "metric languages")
    errors=[]
    for lang in ("en","ja"):
        require(set(actual[lang]) == set(expected[lang]) and actual[lang]["rows"] == expected[lang]["rows"] == 8,
            "metric key/count contract")
        for key,value in actual[lang].items():
            other=expected[lang][key]
            require(type(value) in (int,float) and type(other) in (int,float)
                and math.isfinite(value) and math.isfinite(other), "nonfinite metric")
            errors.append(abs(value-other))
    return max(errors)


def validate_parent_records(records, parent):
    require([(r["seed"],r["family"]) for r in records] == identities(), "parent record order")
    for r in records:
        parent.validate_metrics(r["final_probe"])
        require(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True
            and r["weights_changed"] is True and 0 <= r["reload_max_error"] <= TOL
            and 0 <= r["replay_metric_error"] <= TOL, "parent record integrity")
        require(isinstance(r["final_sha256"],str) and len(r["final_sha256"]) == 64
            and all(c in "0123456789abcdef" for c in r["final_sha256"]), "final fingerprint")
        require(set(r["predictions"]) == set(VIEWS) and all(len(p)==16 and
            all(type(x) is int and 0<=x<256 for x in p) for p in r["predictions"].values()), "parent prediction schema")
    return records


def capture_model(model, rows, views, *, binding, fingerprint):
    """Run the exact parent evaluator twice; passive hooks return no replacement output."""
    require(len(rows)==16 and len(views)==3 and not model.training
        and all(not p.requires_grad for p in model.parameters()), "model not frozen/eval")
    before=fingerprint(model); counts=[0,0]
    def count_hook(module,args,output):
        counts[0]+=1; counts[1]+=len(args[0])
    root_handle=model.register_forward_hook(count_hook)
    handles=[]
    taps={k:[] for k in ("gru","pooled","readout","decoder_input")}
    def gru_hook(module,args,output):
        require(isinstance(output,tuple) and len(output)==2, "GRU output contract")
        taps["gru"].append(output[0].detach().clone())
    def norm_hook(module,args,output):
        taps["pooled"].append(args[0].detach().clone())
        taps["readout"].append(output.detach().clone())
    def decoder_hook(module,args):
        taps["decoder_input"].append(args[0].detach().clone())
    try:
        plain_metrics,plain=binding.evaluate(model,rows,views)
        require(fingerprint(model)==before, "plain evaluation mutation")
        handles.append(model.local_encoder.register_forward_hook(gru_hook))
        handles.append(model.readout_norm.register_forward_hook(norm_hook))
        handles.append(model.decoder.register_forward_pre_hook(decoder_hook))
        captured_metrics,captured=binding.evaluate(model,rows,views)
    finally:
        for handle in handles: handle.remove()
        root_handle.remove()
    require(counts==[6,96] and all(len(v)==3 for v in taps.values()), "capture call counts")
    require(fingerprint(model)==before and not model.training
        and all(p.grad is None and not p.requires_grad for p in model.parameters()), "capture mutation/gradient")
    passive_error=max(float((finite_tensor(x,(16,256))-finite_tensor(y,(16,256))).abs().max())
        for x,y in zip(plain,captured,strict=True))
    require(passive_error<=TOL and prediction_record(plain)==prediction_record(captured)
        and metric_error(plain_metrics,captured_metrics)<=TOL, "passive instrumentation changed output")
    traces={}; reconstruction_error=0.0
    for i,(mode,(tokens,targets)) in enumerate(zip(VIEWS,views,strict=True)):
        indices=eos_indices(tokens)
        encoded=finite_tensor(taps["gru"][i],(16,48,16))
        pooled=finite_tensor(taps["pooled"][i],(16,16))
        readout=finite_tensor(taps["readout"][i],(16,16))
        decoder_input=finite_tensor(taps["decoder_input"][i],(16,16))
        require(torch.equal(readout,decoder_input), "decoder does not read captured norm output")
        with torch.no_grad():
            reconstructed=F.linear(readout,model.decoder.weight,model.decoder.bias)
        error=float((finite_tensor(reconstructed,(16,256))-captured[i]).abs().max())
        require(error<=TOL, "decoder reconstruction failed")
        reconstruction_error=max(reconstruction_error,error)
        traces[mode]=dict(tokens=tokens.clone(),gru_eos=encoded[torch.arange(16),indices],
            pooled=pooled,readout=readout,logits=captured[i].clone())
    return dict(before_sha256=before,after_sha256=fingerprint(model),forward_calls=counts[0],
        row_presentations=counts[1],passive_error=passive_error,reconstruction_error=reconstruction_error,
        metrics=captured_metrics,predictions=prediction_record(captured)),traces


def paired_indices(rows, kind, lang):
    require(kind in PAIR_KINDS and lang in ("en","ja"), "pair mode")
    groups=defaultdict(list)
    for i,r in enumerate(rows):
        if r["language"]!=lang: continue
        if kind=="query": key=(r["group"],r["order"])
        elif kind=="facts": key=(tuple(r["objects"]),tuple(sorted(r["values"])),r["order"],r["query"])
        else: key=(r["group"],r["query"])
        groups[key].append(i)
    require(len(groups)==4 and all(len(g)==2 for g in groups.values()), "pair coverage")
    pairs=[tuple(g) for g in groups.values()]
    for i,j in pairs:
        a,c=rows[i],rows[j]
        require(a["id"]!=c["id"] and (a["target"]==c["target"]) == (kind=="order"), "pair target relation")
        if kind=="query":
            require(a["values"]==c["values"] and a["objects"]==c["objects"] and a["query"]!=c["query"], "query pairing")
        elif kind=="facts": require(a["values"]==list(reversed(c["values"])), "assignment pairing")
        else: require(a["values"]==c["values"] and a["order"]!=c["order"], "order pairing")
    return pairs


def difference(a,c):
    require(a.shape==c.shape and a.numel()>0 and bool(torch.isfinite(a).all())
        and bool(torch.isfinite(c).all()), "contrast tensor")
    delta=(a-c).double(); l2=float(torch.linalg.vector_norm(delta))
    scale=max(float(torch.linalg.vector_norm(a.double())),float(torch.linalg.vector_norm(c.double())))
    return dict(exact_equal=bool(torch.equal(a,c)),linf=float(delta.abs().max()),l2=l2,
        relative_l2=l2/scale if scale else 0.0)


def row_output(logits,target):
    finite_tensor(logits,(256,))
    require(type(target) is int and 0<=target<256, "target byte")
    top=torch.topk(logits,2).values
    return dict(prediction=int(logits.argmax()),target=target,correct=int(logits.argmax())==target,
        digit_margin=float(logits[49]-logits[48]),top_two_gap=float(top[0]-top[1]),
        supplied_probability=float(logits.softmax(-1)[[48,49]].sum()))


def contrast(a,c,i,j,rows,kind):
    return dict(kind=kind,first_id=rows[i]["id"],second_id=rows[j]["id"],
        token_differences=int((a["tokens"][i]!=c["tokens"][j]).sum()),
        differences={key:difference(a[key][i],c[key][j]) for key in LAYERS},
        first=row_output(a["logits"][i],rows[i]["target"]),
        second=row_output(c["logits"][j],rows[j]["target"]))


def contrast_summary(items):
    require(bool(items), "empty contrast summary")
    return dict(count=len(items),input_equal=sum(x["token_differences"]==0 for x in items),
        same_answer=sum(x["first"]["prediction"]==x["second"]["prediction"] for x in items),
        both_correct=sum(x["first"]["correct"] and x["second"]["correct"] for x in items),
        layers={key:dict(exact_equal=sum(x["differences"][key]["exact_equal"] for x in items),
            linf_min=min(x["differences"][key]["linf"] for x in items),
            linf_max=max(x["differences"][key]["linf"] for x in items)) for key in LAYERS},
        digit_margin_change_max=max(abs(x["first"]["digit_margin"]-x["second"]["digit_margin"]) for x in items))


def analyze(rows,traces):
    require(set(traces)==set(VIEWS), "trace views")
    details=[]; cells={}
    for lang in ("en","ja"):
        cell={}
        for kind in PAIR_KINDS:
            items=[contrast(traces["normal"],traces["normal"],i,j,rows,kind) for i,j in paired_indices(rows,kind,lang)]
            for item in items: item["language"]=lang
            details.extend(items); cell[kind]=contrast_summary(items)
        for mode in VIEWS[1:]:
            items=[contrast(traces["normal"],traces[mode],i,i,rows,mode)
                for i,r in enumerate(rows) if r["language"]==lang]
            for item in items: item["language"]=lang
            details.extend(items); cell[mode]=contrast_summary(items)
        cells[lang]=cell
    require(len(details)==56, "contrast count")
    return cells,details


def summarize(records):
    require([(r["seed"],r["family"]) for r in records]==identities(), "diagnostic identity order")
    for r in records:
        require(set(r["cells"])=={"en","ja"}, "diagnostic cell coverage")
        for cell in r["cells"].values():
            require(set(cell)==set(PAIR_KINDS+VIEWS[1:]), "contrast kind coverage")
            for kind,value in cell.items(): require(value["count"]==(4 if kind in PAIR_KINDS else 8), "contrast workload")
    return dict(models=6,diagnostic_cells=12,model_forward_calls=sum(r["forward_calls"] for r in records),
        row_presentations=sum(r["row_presentations"] for r in records),paired_contrasts=144,masked_row_contrasts=192,
        all_fingerprints_unchanged=all(r["before_sha256"]==r["after_sha256"] for r in records),
        all_parent_replays=all(r["parent_predictions_equal"] is True and 0<=r["parent_metric_error"]<=TOL for r in records),
        all_passive_replays=all(0<=r["passive_error"]<=TOL and 0<=r["reconstruction_error"]<=TOL for r in records),
        new_training_steps=0,capability_pass_claim=False,causal_claim=False)


def validate_result(result):
    require(result["experiment_id"]==EXPERIMENT_ID and result["stage"]==STAGE and result["status"]=="PASS"
        and result["diagnostic_execution_valid"] is True, "diagnostic identity/status")
    require((len(result["source_blobs"]),len(result["input_sha256"]))==(268,394)
        and set(OWN)<=set(result["source_blobs"]), "source/input protection")
    require(len(result["artifacts"])==5 and {x["file"] for x in result["artifacts"]}==OUTPUTS, "artifact coverage")
    s=result["validation_summary"]
    require((s["models"],s["diagnostic_cells"],s["model_forward_calls"],s["row_presentations"],
        s["paired_contrasts"],s["masked_row_contrasts"],s["new_training_steps"])==(6,12,36,576,144,192,0), "fixed workload")
    require(s["all_fingerprints_unchanged"] is True and s["all_parent_replays"] is True
        and s["all_passive_replays"] is True, "replay/fingerprint integrity")
    require(s["capability_pass_claim"] is False and s["causal_claim"] is False
        and result["gate_f_candidate"] is False and result["network_calls"]==0, "claim scope")


def precheck(c236_summary,root):
    parent,binding,factory,a=context(); root=Path(root); c236_summary=Path(c236_summary).resolve()
    require(a.sha(c236_summary)==PARENT_SHA, "parent summary identity")
    p=a.read_json(c236_summary); parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL"
        and p["validation_summary"]["full_probe_gate"] is False
        and p["validation_summary"]["gru_probe_gate"] is False, "accepted negative parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items(): require(Path(path).is_file() and a.sha(path)==wanted,"changed input:"+path)
    for path,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+path).decode().strip()==wanted,"changed source:"+path)
    require(str(c236_summary) not in protected, "parent summary double count")
    protected[str(c236_summary)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifact identities")
    for item in p["artifacts"]:
        path=a.safe_child(c236_summary.parent,item["file"])
        require(a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
        require(str(path.resolve()) not in protected,"parent artifact double count")
        protected[str(path.resolve())]=item["sha256"]
    for path in OWN:
        require(path not in pins,"OWN collision")
        pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    deps=set(factory.LM_SOURCES)|{OWN[0],
        "fold_lm/v05_benchmarks/model_c236_minimal_binding.py",
        "fold_lm/v05_benchmarks/model_c235_frozen_binding_diagnostic.py",
        "fold_lm/v05_benchmarks/model_c234_context_binding.py",
        "fold_lm/v05_benchmarks/model_c233_core_ablation.py",
        "fold_lm/v05_benchmarks/model_c232_bilingual_learning.py",
        "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
        "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"}
    require(len(deps)==13 and deps<=set(pins),"direct dependency coverage")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(268,394),"protection counts")
    require(digest(manifest())==MANIFEST_SHA,"manifest mismatch")
    return pins,protected


def load_inputs(c236_summary):
    parent,_,_,a=context(); directory=Path(c236_summary).resolve().parent
    rows=a.read_json(directory/"probe-dataset.json")
    require(len(rows)==16 and digest(rows)==PARENT_ARTIFACTS["probe-dataset.json"],"probe cohort identity")
    records=validate_parent_records(a.read_json(directory/"measurements.json"),parent)
    require(parent.summarize(records)==a.read_json(c236_summary)["validation_summary"],"parent measurement summary")
    states=parent.load_bundle(directory/"trained-models.pt")
    return rows,records,states


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==121,"parent regression modules")
    return names+["tests_lm.test_v05_c237_frozen_signal_audit"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"historical test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(2858,2857),"regression counts")
    return unittest.TestSuite(kept)


def run(*,c236_summary,output_dir,expected_head):
    parent,binding,factory,a=context(); root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch mismatch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tracked tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c236_summary,root)
    rows,saved,states=load_inputs(c236_summary)
    views=[binding.tensors(rows,mode) for mode in VIEWS]
    records=[]; all_traces=[]; all_details=[]
    for index,((seed,family),reference,state) in enumerate(zip(identities(),saved,states,strict=True),1):
        print(f"[C237] model={index}/6 seed={seed} family={family}; frozen capture/replay",flush=True)
        model=factory.new_model(seed)
        if family=="gru_only": model=binding.parent_module().new_baseline(model)
        model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
        require(factory.fingerprint(model)==reference["final_sha256"],"accepted final fingerprint")
        record,traces=capture_model(model,rows,views,binding=binding,fingerprint=factory.fingerprint)
        parent_error=metric_error(record["metrics"],reference["final_probe"])
        parent_equal=record["predictions"]==reference["predictions"]
        require(parent_error<=TOL and parent_equal,"C236 final replay mismatch")
        cells,details=analyze(rows,traces)
        record.update(seed=seed,family=family,parent_metric_error=parent_error,parent_predictions_equal=parent_equal,cells=cells)
        records.append(record)
        all_traces.append(dict(seed=seed,family=family,views={mode:{k:v.tolist() for k,v in part.items()} for mode,part in traces.items()}))
        all_details.append(dict(seed=seed,family=family,contrasts=details))
    summary=summarize(records)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for name,value in (("diagnostic-plan.json",manifest()),("traces.json",all_traces),
        ("contrasts.json",all_details),("diagnostics.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c236_summary,root)
    for path,wanted in protected.items(): require(a.sha(path)==wanted,"modified input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,network_calls=0,
        limitations=["Numerical sensitivity is not causal attribution or learned binding.",
            "Exact equality is a finite-precision observation, not information-theoretic impossibility.",
            "Cross-layer scale differences do not identify the cause of training failure."])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C237 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result



def verify_artifacts(output_dir,c236_summary,expected_head):
    """Recompute persisted contrasts without extra model forwards or training."""
    _,binding,_,a=context(); out=Path(output_dir)
    result=a.read_json(out/"summary.json"); validate_result(result)
    require(result["commit_sha"]==expected_head,"summary execution identity")
    for name,wanted in result["input_sha256"].items(): require(a.sha(name)==wanted,"postcheck input:"+name)
    for item in result["artifacts"]:
        path=a.safe_child(out,item["file"])
        require(a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"postcheck artifact")
    records=a.read_json(out/"diagnostics.json")
    require(summarize(records)==result["validation_summary"],"diagnostic summary mismatch")
    require(a.read_json(out/"validation-summary.json")==result["validation_summary"],"saved validation mismatch")
    require(a.read_json(out/"diagnostic-plan.json")==manifest(),"saved plan mismatch")
    source_rows=a.read_json(Path(c236_summary).resolve().parent/"probe-dataset.json")
    require(digest(source_rows)==PARENT_ARTIFACTS["probe-dataset.json"],"postcheck cohort")
    views=[binding.tensors(source_rows,mode) for mode in VIEWS]
    stored=a.read_json(out/"traces.json"); details=a.read_json(out/"contrasts.json")
    require([(x["seed"],x["family"]) for x in stored]==identities()
        and [(x["seed"],x["family"]) for x in details]==identities(),"trace/contrast identities")
    for record,saved,expected in zip(records,stored,details,strict=True):
        traces={mode:{key:torch.tensor(value,dtype=torch.int64 if key=="tokens" else torch.float64)
            for key,value in part.items()} for mode,part in saved["views"].items()}
        require(set(traces)==set(VIEWS),"saved views")
        for mode,view in zip(VIEWS,views,strict=True):
            require(set(traces[mode])==set(LAYERS)|{"tokens"},"saved layer set")
            eos_indices(traces[mode]["tokens"])
            require(torch.equal(traces[mode]["tokens"],view[0]),"saved input changed")
            for key in LAYERS: finite_tensor(traces[mode][key],(16,256 if key=="logits" else 16))
        cells,contrasts=analyze(source_rows,traces)
        require(cells==record["cells"] and contrasts==expected["contrasts"],"saved contrast replay")
        logits=[traces[mode]["logits"] for mode in VIEWS]
        require(prediction_record(logits)==record["predictions"],"saved prediction replay")
    return result,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c236-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
