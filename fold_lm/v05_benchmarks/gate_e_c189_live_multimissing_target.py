"""C189: frozen learned multi-missing target -> one real acquisition -> live reclassification.

Diagnostic only. Reuse all nine accepted C188 selector heads and their three frozen
C181 INTERNAL_SEMANTICS bases. The initial necessity decision and learned target
selection share one base forward. Exactly one RETRIEVE may execute; post state is
reclassified once and never triggers a second acquisition.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch import nn

EXPERIMENT_ID = "C189-v5e-live-multimissing-target-acquisition"
STAGE = "V5-E-LIVE-MULTIMISSING-TARGET-ACQUISITION"
BASE = "2edadff6f8fab1c3c26da46adee630d12e433be8"
PARENT_EXECUTION = "683d795b12d4f0aada4850dcac2a010e699882ad"
PARENT_SHA = "2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153"
BASE_SEEDS = (181001, 181002, 181003)
HEAD_SEEDS = (188001, 188002, 188003)
ARM = "INTERNAL_SEMANTICS"
BITS = (0, 1)
BATCH = 1024
PRIOR_NAMES = ("c188","c187","c186","c185","c184","c183","c182","c181","c180",
               "c179","c178","c177","c176","c174")
OWN = ("fold_lm/v05_benchmarks/gate_e_c189_live_multimissing_target.py",
       "tests_lm/test_v05_c189_live_multimissing_target.py",
       "tools/run_c189.ps1",
       "docs/experiment-ledger-addendum-c189-preregistration.md")
SOURCES = {
    "sources/fact-0-completion-0.json": "d3d693b1ce3d22b31f3826feace8eb511eb3e8f5b427ba1ac2fb607af8419dc2",
    "sources/fact-1-completion-0.json": "1b6b28bab6436fb62dac757d629d4eda6da45c098f70f5f3414a6b1afc9fd292",
    "sources/fact-2-completion-0.json": "ff89d9d08d5cf91452059f835997a2001c2c27e39a341e35294a28c564beca5b",
    "sources/fact-3-completion-0.json": "6182708e781d9f0f73cd3df20c1257a9611d8d3ed02f4499992e700545b249c2",
    "sources/fact-0-completion-1.json": "aa684e21cc075142892e05a65d260a3967abde5da7b3996d58b924df7df8f7d6",
    "sources/fact-1-completion-1.json": "43984ace8084b91f3bb8ec74c1da6f97b3ff95a988fe62373f7a07647ceb3e56",
    "sources/fact-2-completion-1.json": "d6fb4451badea2e3d8fe8bceb80464c891efae5f7323c150959c9eca5e2b70c",
    "sources/fact-3-completion-1.json": "09c4b6c269cbfbf1ab3c9cf9ce22cdcd5ded0abbf2fd601d8a1e50be2a6e9ea9",
}
OUTPUTS = {"live-target-plan.json","selector-replay.json","episode-results.json",
           "episode-traces.jsonl.gz","episode-predictions.npz"} | set(SOURCES)
ATOL = 1e-6
EXPECTED_TESTS = 1449

def require(ok, message):
    if not ok:
        raise ValueError(message)

def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()

def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()

def source_bytes(fact_index, bit):
    require(type(fact_index) is int and 0 <= fact_index < 4 and type(bit) is int and bit in BITS,
            "Registered source identity required")
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    data=driver.fixture_bytes(fact_index,bit)
    name=f"sources/fact-{fact_index}-completion-{bit}.json"
    require(hashlib.sha256(data).hexdigest()==SOURCES[name], "Registered source bytes drift")
    return data

def encode_views(views):
    """Direct original C174 numeric layout; no C184 renaming/canonicalization in C189."""
    from fold_lm.v05 import structured_task_input as task
    require(type(views) is list and views, "Nonempty view batch required")
    packets=[task.encode(v) for v in views]
    require(all(task.decode(p)==v for p,v in zip(packets,views,strict=True)), "TaskView roundtrip drift")
    raw=torch.tensor([p.features for p in packets],dtype=torch.int32)
    require(raw.shape==(len(views),72), "Policy packet width drift")
    return raw,packets

def restore_selector(path, base_seed, head_seed, expected_sha):
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as parent
    require((base_seed,head_seed) in {(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS},
            "Unregistered selector identity")
    p=torch.load(path,map_location="cpu",weights_only=True)
    require((p["base_seed"],p["head_seed"],p["schema"],p["feature_width"],p["steps"]) ==
            (base_seed,head_seed,"c188-target-selector-v1",parent.FEATURES,parent.STEPS),
            "Selector checkpoint metadata drift")
    model=parent.TargetSelector()
    model.load_state_dict(p["state_dict"],strict=True); model.eval()
    require(parent.head_fingerprint(model)==p["head_sha256"]==expected_sha,
            "Selector checkpoint fingerprint drift")
    return model

def load_parent_predictions(path):
    """Small accepted C188 NPZ only; hash/size already protected before materialization."""
    p=Path(path)
    require(p.is_file() and p.stat().st_size < 2_000_000, "Unexpected C188 prediction artifact size")
    with np.load(p,allow_pickle=False) as z:
        require(set(z.files)=={"row_indices","predictions","logits","base_seeds","head_seeds"},
                "C188 prediction schema drift")
        out={k:z[k].copy() for k in z.files}
    require(out["row_indices"].shape==(1768,) and out["row_indices"].dtype.kind in "iu"
            and out["predictions"].shape==(9,1768)
            and out["logits"].shape==(9,1768,4) and out["logits"].dtype==np.float32
            and out["base_seeds"].tolist()==[b for b in BASE_SEEDS for _ in HEAD_SEEDS]
            and out["head_seeds"].tolist()==[h for _ in BASE_SEEDS for h in HEAD_SEEDS],
            "C188 prediction array drift")
    require(set(np.unique(out["predictions"]).tolist()) <= {0,1,2,3}, "Invalid saved target prediction")
    return out

def combined_predict(base, selector, raw, *, batch=BATCH):
    """One frozen base forward emits necessity plus hidden states used by the target head."""
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    require(type(base) is graph.SharedGraphProbe and base.arm==graph.ARMS[1], "Frozen TREE_LINKS base required")
    require(type(selector) is target.TargetSelector and type(batch) is int and batch>0, "Frozen target head required")
    target.missing_mask(raw); pos=target.leaf_positions(raw); scaled=binding.prepare_pair(raw)[1]
    unknown=target.missing_mask(raw)
    bfp,hfp=graph.fingerprint(base),target.head_fingerprint(selector)
    old=(base.calls,base.cell_calls,base.rows); nz=[];tz=[]
    started=time.perf_counter()
    with torch.inference_mode():
        for lo in range(0,len(raw),batch):
            hi=min(len(raw),lo+batch); states=[]
            handle=base.cell.register_forward_hook(lambda module,args,output: states.append(output.detach()))
            try:
                nlogit=base(scaled[lo:hi])
            finally:
                handle.remove()
            require(len(states)==7 and nlogit.shape==(hi-lo,2) and torch.isfinite(nlogit).all().item(),
                    "Combined base forward drift")
            bank=torch.stack(states,dim=1)
            flat=bank.reshape(hi-lo,-1)[:,None,:].expand(-1,4,-1)
            one=nn.functional.one_hot(pos[lo:hi],num_classes=7).to(torch.float32)
            feature=torch.cat((flat,one),dim=2)
            tlogit=selector(feature)
            tlogit=tlogit.masked_fill(~unknown[lo:hi],float("-inf"))
            require(torch.isfinite(tlogit[unknown[lo:hi]]).all().item()
                    and torch.isneginf(tlogit[~unknown[lo:hi]]).all().item(),
                    "Target score masking/nonfinite drift")
            nz.append(nlogit.cpu()); tz.append(tlogit.cpu())
    nlogit=torch.cat(nz); tlogit=torch.cat(tz)
    calls=(len(raw)+batch-1)//batch
    require(graph.fingerprint(base)==bfp and target.head_fingerprint(selector)==hfp
            and (base.calls-old[0],base.cell_calls-old[1],base.rows-old[2])==(calls,7*calls,len(raw)),
            "Frozen combined inference mutated weights/meters")
    return (nlogit.argmax(1).numpy().astype(np.int8),
            tlogit.argmax(1).numpy().astype(np.int8),
            nlogit.numpy(),tlogit.numpy(),
            dict(rows=len(raw),forward_calls=calls,cell_calls=7*calls,
                 wall_clock_seconds=time.perf_counter()-started))

def necessity_predict(base, raw, *, batch=BATCH):
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    p,z,m=graph.predict(base,binding.prepare_pair(raw)[1],batch=batch)
    return p.numpy().astype(np.int8),z.numpy(),m

def target_teacher(features, template_ids, metadata):
    """Scoring/training-label logic only; never passed to policy or transport."""
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as parent
    return parent.influence_masks(features,template_ids,metadata)

def post_label(row, template_id, metadata):
    from fold_lm.v05_benchmarks import gate_e_c174_learned_necessity as c174
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as parent
    vis=parent.visible_tuple(row)
    table=tuple(int(v) for v in metadata[int(template_id)]["truth_table"])
    return int(c174.label_for(table,vis))

def bind_selected_endpoint(owner, endpoints, target_index):
    """Trusted runtime wiring after learned target selection; preserve exact RuntimeState."""
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    require(type(target_index) is int and 0 <= target_index < 4, "Local target index required")
    view=owner.state.view
    require(view.facts[target_index].status=="UNOBSERVED", "Selected endpoint target must be unknown")
    fid=view.facts[target_index].fact_id
    require(fid in endpoints and type(endpoints[fid]) is life.Endpoint, "Selected target endpoint unavailable")
    state=owner.state
    rebound=life.AcquisitionOwner(state,{"RETRIEVE":endpoints[fid]},max_dispatches=1)
    require(rebound.state==state, "Endpoint binding changed RuntimeState")
    return rebound

def acquire_selected(owner, target_index):
    """C172/C173 execute the raw learned local target; no target repair."""
    from fold_lm.v05 import structured_action_runtime as action
    require(type(target_index) is int and 0<=target_index<4, "Local target index required")
    view=owner.state.view
    require(view.facts[target_index].status=="UNOBSERVED", "Learned target must currently be unknown")
    fid=view.facts[target_index].fact_id
    tr=owner.apply(action.propose(owner.state,"RETRIEVE",fact_index=target_index))
    dispatched=None
    if tr.result.status=="PENDING":
        dispatched=owner.dispatch(tr.result.intent.intent_id)
    return dict(input_index=target_index,fact_id=fid,action=asdict(tr.result),
                dispatch=asdict(dispatched) if dispatched else None)

def run_block(views, endpoints, base, selector):
    """Independent episodes; one shared initial decision, max one real acquisition, one post necessity decision."""
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    require(views and all(sum(f.status=="UNOBSERVED" for f in v.facts) in (2,3) for v in views),
            "C189 requires initial missing2/3 rows")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=1) for v in views]
    n=len(views)
    records=[dict(initial=asdict(task.encode(v)),
                  phases=[],acquisition=None,decision_charges=0,status="UNRESOLVED") for v in views]
    n_pred=np.full((n,2),-1,dtype=np.int8); n_logits=np.zeros((n,2,2),dtype=np.float32)
    t_pred=np.full(n,-1,dtype=np.int8); t_logits=np.full((n,4),-np.inf,dtype=np.float32)
    meter=dict(rows=0,forward_calls=0,cell_calls=0)

    active=[i for i,o in enumerate(owners) if driver.charge_decision(o)]
    require(len(active)==n, "Initial decision budget unexpected")
    raw,packets=encode_views([owners[i].state.view for i in active])
    p,t,z,tz,m=combined_predict(base,selector,raw)
    for k in meter: meter[k]+=m[k]
    for j,i in enumerate(active):
        n_pred[i,0]=p[j]; n_logits[i,0]=z[j]; t_pred[i]=t[j]; t_logits[i]=tz[j]
        records[i]["decision_charges"]+=1
        records[i]["phases"].append(dict(phase=0,packet=asdict(packets[j]),
            necessity_prediction=int(p[j]),target_prediction=int(t[j])))
    post=[]
    for i in active:
        if n_pred[i,0]==0:
            records[i]["status"]="SUFFICIENT_CLASSIFICATION"
        else:
            owners[i]=bind_selected_endpoint(owners[i],endpoints,int(t_pred[i]))
            records[i]["acquisition"]=acquire_selected(owners[i],int(t_pred[i]))
            post.append(i)

    post_active=[i for i in post if driver.charge_decision(owners[i])]
    require(len(post_active)==len(post), "Post decision budget unexpectedly exhausted")
    if post_active:
        raw2,packets2=encode_views([owners[i].state.view for i in post_active])
        p2,z2,m2=necessity_predict(base,raw2)
        for k in meter: meter[k]+=m2[k]
        for j'3%¶¥Ò’À¢æV6W76—G•÷&VF–7F–öãÖ–çB‡%¶¥Ò’’¢&V6÷&G5¶•Õ²'7FGW2%ÓÒ%5Tdd”4”TåEô4Ä54”d”4D”ôâ"–b%¶¥ÓÓÓVÇ6R%Tå$U4ôÅdTB  ¢f÷"’Æò–âVçVÖW&FR†÷væW'2“ ¢&V6÷&G5¶•Õ²&f–æÂ%ÓÖ6F–7B‡F6²æVæ6öFR†òç7FFRçf–Wr’¢&V6÷&G5¶•Õ²'&V6V—G2%ÓÕ¶6F–7B‡"’f÷""–âòç&V6V—G5Ð¢&V6÷&G5¶•Õ²'VæF–ær%ÓÖ6F–7B†òç7FFRçVæF–ær’–bòç7FFRçVæF–ærVÇ6RæöæP¢&V6÷&G5¶•Õ²''VçF–ÖU÷FW&Ö–æÂ%ÓÖòç7FFRçFW&Ö–æÀ¢&WGW&â&V6÷&G2ÆF–7B†æV6W76—G•÷&VF–7F–öç3Öå÷&VBÆæV6W76—G•öÆöv—G3ÖåöÆöv—G2À¢F&vWE÷&VF–7F–öç3×E÷&VBÇF&vWEöÆöv—G3×EöÆöv—G2’ÆÖWFW  ¦FVb76W72‡&V6÷&BÂfÆ–E÷F&vWG2Â6÷W&6U÷&÷rÂFV×ÆFUö–BÂÖWFFFÂ&—BÂ&VçE÷F&vWB“ ¢""%÷7BÖ†ö266÷&–æröæÇ’âæWfW"6†ævW2F&vWBÂ7F–öâÂWf–FVæ6R÷"&VF–7F–öââ"" ¢&WV—&R‡G—R†&—B’—2–çBæB&—B–â$•E2æBG—R‡&VçE÷F&vWB’–â†–çBÆçæ–çC‚Æçæ–çCbÆçæ–çC3"Æçæ–çCcB’À¢%&Vv—7FW&VB66÷&–ær–çWG2&WV—&VB"¢–æ—F–ÂÆf–æÃ×&V6÷&E²&–æ—F–Â%ÒÇ&V6÷&E²&f–æÂ%Ð¢ƒÖçæ6'&’†–æ—F–Å²&fVGW&W2%ÒÆGG—SÖçæ–çCcB“²cÖçæ6'&’†f–æÅ²&fVGW&W2%ÒÆGG—SÖçæ–çCcB¢†6W3×&V6÷&E²'†6W2%Ð¢×†6W5³Õ²&æV6W76—G•÷&VF–7F–öâ%Ò–b†6W2VÇ6RÓ¢F&vWC×†6W5³Õ²'F&vWE÷&VF–7F–öâ%Ò–b†6W2VÇ6RÓ¢÷7C×†6W5³Õ²&æV6W76—G•÷&VF–7F–öâ%Ò–bÆVâ‡†6W2“ãVÇ6RÓ¢F&vWEöö³ÓÃ×F&vWCÃBæB&ööÂ‡fÆ–E÷F&vWG5·F&vWEÒ¢F&vWE÷&WÆ•öö³×F&vWCÓÖ–çB‡&VçE÷F&vWB¢×&V6÷&E²&7V—6—F–öâ%Ó²CÖ²&F—7F6‚%Ò–bVÇ6RæöæP¢&W6W'fVCÖ²&7F–öâ%Õ²&7V—6—F–öå÷&W6W'fVB%Ò–bVÇ6R ¢6ÆÇ3ÖE²'&÷f–FW%ö6ÆÇ2%Ò–bBVÇ6R ¢V'3ÖE²&f7E÷V&Æ–6F–öç2%Ò–bBVÇ6R ¢&V6V—G3×&V6÷&E²'&V6V—G2%Ð¢6VÆV7FVEöf–CÖ–æ—F–Å²&&–æF–ær%Õ²&f7Eö–G2%Õ·F&vWEÒ–bÃ×F&vWCÃBVÇ6RæöæP¢7G'V7GW&ÃÕG'VP¢–b—2æöæS ¢7G'V7GW&ÃÒ‡ÓÓæBæ÷B&V6V—G2æB6ÆÇ3Ó×V'3Ó×&W6W'fVCÓÓ ¢æB&V6÷&E²'7FGW2%ÓÓÒ%5Tdd”4”TåEô4Ä54”d”4D”ôâ"¢VÇ6S ¢7G'V7GW&ÃÒ‡F&vWEöö²æB²&–çWEö–æFW‚%ÓÓ×F&vWBæB²&f7Eö–B%ÓÓ×6VÆV7FVEöf–@¢æB²&7F–öâ%Õ²'7FGW2%ÓÓÒ%TäD”är"æB²&7F–öâ%Õ²'&V6öâ%ÓÓÒ$5T•4•D”ôåõ$U4U%dTB ¢æB²&7F–öâ%Õ²&–çFW&æÅö6†&vVB%ÓÓÓæB&W6W'fVCÓÓ¢æBB—2æ÷BæöæRæBE²'7FGW2%ÓÓÒ%T$Ä•4„TB"æBE²'&V6öâ%ÓÓÒ$ô%4U%dD”ôåôDÔ•EDTB ¢æBE²&–çFW&æÅö6†&vVB%ÓÓÓ"æB6ÆÇ3Ó×V'3ÓÓ¢æBÆVâ‡&V6V—G2“ÓÓæB&V6V—G5³Õ²&f7Eö–B%ÓÓ×6VÆV7FVEöf–@¢æB&V6V—G5³Õ²'fÇVR%ÓÓÖ&—BæB&V6V—G5³Õ²&7F–öâ%ÓÓÒ%$UE$”UdR ¢æB&V6V—G5³Õ²'&WVW7Eö–B%ÓÓÖ–æ—F–Å²&&–æF–ær%Õ²'&WVW7Eö–B%Ð¢æB&V6V—G5³Õ²'66÷Uö–B%ÓÓÖ–æ—F–Å²&&–æF–ær%Õ²'66÷Uö–B%Ð¢æBE²&Wf–FVæ6R%ÓÓ×&V6V—G5³Ò¢–b7G'V7GW&Ã ¢7G'V7GW&Ã×7G'V7GW&ÂæBÆ—7B†e³Cb³B§F&vWC£S³B§F&vWEÒ“ÓÕ³Ã"ÃÆ&—EÐ¢f÷"¢–â&ævRƒB“ ¢–b¢×F&vWC ¢7G'V7GW&Ã×7G'V7GW&ÂæBçæ'&•öWVÂ†e³Cb³B¦££S³B¦¥ÒÇ…³Cb³B¦££S³B¦¥Ò¢7G'V7GW&Ã×7G'V7GW&ÂæBf–æÅ²&&–æF–ær%Õ²'&VfW&Væ6Uö–G2%Õ¶¥ÓÓÖ–æ—F–Å²&&–æF–ær%Õ²'&VfW&Væ6Uö–G2%Õ¶¥Ð¢7G'V7GW&Ã×7G'V7GW&ÂæBÆ—7B†f–æÅ²&&–æF–ær%Õ²'&VfW&Væ6Uö–G2%Õ·F&vWEÒ“ÓÕ·&V6V—G5³Õ²'&VfW&Væ6Uö–B%ÕÐ¢6†&vW3×&V6÷&E²&FV6—6–öåö6†&vW2%Ò²†²&7F–öâ%Õ²&–çFW&æÅö6†&vVB%Ò–bVÇ6R’²†E²&–çFW&æÅö6†&vVB%Ò–bBVÇ6R¢7G'V7GW&Ã×7G'V7GW&ÂæB†e³c%ÓÓ×…³c%ÒÖ6†&vW2æBe³c5ÓÓ×…³c5Ò×&W6W'fVBæBe³sÓÓ×…³sÒ¶6†&vW2¢–b—2æ÷BæöæS ¢7G'V7GW&Ã×7G'V7GW&ÂæB&V6÷&E²&FV6—6–öåö6†&vW2%ÓÓÓ ¢2W&Ö—76–öâöf–Æ&–Æ—G’f–VÆG2&RVæ6†ævVC²Æ7Eö÷WF6öÖRÖ’6†ævRgFW"FÖ—76–öâà¢7G'V7GW&Ã×7G'V7GW&ÂæBçæ'&•öWVÂ†e³cC£sÒÇ…³cC£sÒ¢7G'V7GW&Ã×7G'V7GW&ÂæBçæ'&•öWVÂ†e³£CeÒÇ…³£CeÒ¢7G'V7GW&Ã×7G'V7GW&ÂæB–æ—F–Å²&&–æF–ær%Õ²&f7Eö–G2%ÓÓÖf–æÅ²&&–æF–ær%Õ²&f7Eö–G2%Ð¢7G'V7GW&Ã×7G'V7GW&ÂæB–æ—F–Å²&&–æF–ær%Õ²'&WVW7Eö–B%ÓÓÖf–æÅ²&&–æF–ær%Õ²'&WVW7Eö–B%Ð¢7G'V7GW&Ã×7G'V7GW&ÂæB–æ—F–Å²&&–æF–ær%Õ²'66÷Uö–B%ÓÓÖf–æÅ²&&–æF–ær%Õ²'66÷Uö–B%Ð¢7G'V7GW&Ã×7G'V7GW&ÂæB&V6÷&E²'VæF–ær%Ò—2æöæRæB&V6÷&E²''VçF–ÖU÷FW&Ö–æÂ%Ò—2æöæP¢W‡V7FVE÷÷7C×÷7EöÆ&VÂ†f–æÅ²&fVGW&W2%ÒÇFV×ÆFUö–BÆÖWFFF’–b—2æ÷BæöæRæBV'3ÓÓVÇ6RæöæP¢÷7EöW'&÷#Ö–çB†W‡V7FVE÷÷7B—2æöæR÷"÷7BÖW‡V7FVE÷÷7B’–b—2æ÷BæöæRVÇ6R ¢7FGW5öö³Ò‡&V6÷&E²'7FGW2%ÓÓÒ‚%5Tdd”4”TåEô4Ä54”d”4D”ôâ"–b÷7CÓÓVÇ6R%Tå$U4ôÅdTB"’’–b—2æ÷BæöæRVÇ6RG'VP¢7G'V7GW&Ã×7G'V7GW&ÂæB7FGW5öö°¢–æ—F–ÅöW'&÷#Ö–çB‡Ó¢F&vWEöW'&÷#Ö–çB†æ÷BF&vWEöö²¢F&vWE÷&WÆ•öW'&÷#Ö–çB†æ÷BF&vWE÷&WÆ•öö²¢Ö—76VCÖ–çB†—2æöæR÷"6ÆÇ2Ó÷"V'2Ó¢6öçG&7CÖ–çB†æ÷B7G'V7GW&Â¢&WGW&âF–7B†f–ÆVCÖ–çB†&ööÂ†–æ—F–ÅöW'&÷"÷"F&vWEöW'&÷"÷"F&vWE÷&WÆ•öW'&÷"÷"Ö—76VB÷"÷7EöW'&÷"÷"6öçG&7B’’À¢–æ—F–ÅöW'&÷#Ö–æ—F–ÅöW'&÷"ÇF&vWEöW'&÷#×F&vWEöW'&÷"ÇF&vWE÷&WÆ•öW'&÷#×F&vWE÷&WÆ•öW'&÷"À¢6VÆV7FVEöö'6W'fVCÖ–çBƒÃ×F&vWCÃBæB…³C‚³B§F&vWEÓÓÓ’À¢Ö—76VEö7V—6—F–öãÖÖ—76VBÇ÷7EöW'&÷#×÷7EöW'&÷"Æ6öçG&7EöW'&÷#Ö6öçG&7BÀ¢÷7EöW‡V7FVCÒÓ–bW‡V7FVE÷÷7B—2æöæRVÇ6R–çB†W‡V7FVE÷÷7B’À¢÷7E÷&VF–7F–öãÖ–çB‡÷7B’Ç&W6W'fF–öç3Ö–çB‡&W6W'fVB’Ç&÷f–FW%ö6ÆÇ3Ö–çB†6ÆÇ2’À¢V&Æ–6F–öç3Ö–çB‡V'2’ÆFV6—6–öåö6†&vW3Ö–çB‡&V6÷&E²&FV6—6–öåö6†&vW2%Ò’Æ–çFW&æÅö6†&vVCÖ–çB†6†&vW2’ ¤4õTåDU%3Ò‚&f–ÆVB"Â&–æ—F–ÅöW'&÷""Â'F&vWEöW'&÷""Â'F&vWE÷&WÆ•öW'&÷""Â'6VÆV7FVEöö'6W'fVB"À¢&Ö—76VEö7V—6—F–öâ"Â'÷7EöW'&÷""Â&6öçG&7EöW'&÷""Â'&W6W'fF–öç2"Â'&÷f–FW%ö6ÆÇ2"À¢'V&Æ–6F–öç2"Â&FV6—6–öåö6†&vW2"Â&–çFW&æÅö6†&vVB" ¦FVbW‡V7FVEö÷&FW"‚“ ¢&WGW&â²†"Æ‚Æ&—B’f÷""–â$4Uõ4TTE2f÷"‚–â„TEõ4TTE2f÷"&—B–â$•E5Ð ¦FVbvFR‡&V6÷&G2Â&WÆ’“ ¢–b²‡"ævWB‚&&6U÷6VVB"’Ç"ævWB‚&†VE÷6VVB"’Ç"ævWB‚&6ö×ÆWF–öâ"’’f÷""–â&V6÷&G5ÒÒW‡V7FVEö÷&FW"‚“ ¢&WGW&âfÇ6P¢–bæ÷B—6–ç7Fæ6R‡&WÆ’ÆÆ—7B’÷"²‡"ævWB‚&&6U÷6VVB"’Ç"ævWB‚&†VE÷6VVB"’’f÷""–â&WÆ•ÒÒ°¢†"Æ‚’f÷""–â$4Uõ4TTE2f÷"‚–â„TEõ4TTE5Ó ¢&WGW&âfÇ6P¢–bç’‡"ævWB‚'&VF–7F–öç5öWVÂ"’—2æ÷BG'VR÷ ¢æ÷B—6–ç7Fæ6R‡"ævWB‚&Ö…ö'5öÆöv—EöF–ffW&Væ6R"’Â†–çBÆfÆöB’’÷ ¢æ÷Bçæ—6f–æ—FR‡%²&Ö…ö'5öÆöv—EöF–ffW&Væ6R%Ò’÷"%²&Ö…ö'5öÆöv—EöF–ffW&Væ6R%ÓäDôÂf÷""–â&WÆ’“ ¢&WGW&âfÇ6P¢f÷""–â&V6÷&G3 ¢–b"ævWB‚&W—6öFW2"’Ósc‚÷""ævWB‚&F—67&–Ö–æF–æu÷&÷w2"’ÓS#ƒ ¢&WGW&âfÇ6P¢–bç’‡G—R‡"ævWB†²’’—2æ÷B–çB÷"%¶µÓÃf÷"²–â4õTåDU%2“ ¢&WGW&âfÇ6P¢–bç’‡%¶µÒÓf÷"²–â‚&f–ÆVB"Â&–æ—F–ÅöW'&÷""Â'F&vWEöW'&÷""Â'F&vWE÷&WÆ•öW'&÷""À¢'6VÆV7FVEöö'6W'fVB"Â&Ö—76VEö7V—6—F–öâ"Â'÷7EöW'&÷""Â&6öçG&7EöW'&÷""’“ ¢&WGW&âfÇ6P¢–b‡%²'&W6W'fF–öç2%ÒÇ%²'&÷f–FW%ö6ÆÇ2%ÒÇ%²'V&Æ–6F–öç2%Ò’Òƒsc‚Ãsc‚Ãsc‚“ ¢&WGW&âfÇ6P¢–b%²&FV6—6–öåö6†&vW2%ÒÓ3S3b÷"%²&–çFW&æÅö6†&vVB%ÒÓƒƒC ¢&WGW&âfÇ6P¢–b"ævWB‚&F—67&–Ö–æF–æu÷F&vWEöW'&÷'2"’Ó ¢&WGW&âfÇ6P¢C×"ævWB‚&–æ—F–Å÷F&vWEöÖ…ö'5öÆöv—EöF–ffW&Væ6R"¢–bæ÷B—6–ç7Fæ6R†BÂ†–çBÆfÆöB’’÷"æ÷Bçæ—6f–æ—FR†B’÷"CäDôÃ ¢&WGW&âfÇ6P¢–b"ævWB‚'÷7E÷7Vff–6–VçB"Ã’·"ævWB‚'÷7EöæVVG2"Ã’Óscƒ ¢&WGW&âfÇ6P¢&WGW&âG'VP ¦FVbÖæ–fW7B‚“ ¢&WGW&âF–7B†W‡W&–ÖVçEö–CÔU…U$”ÔTåEô”BÇ7FvSÕ5DtRÇ&VçE÷6†#ScÕ$TåEõ4„À¢66WFæ6Uö&6SÔ$4RÇ&VçEöW†V7WF–öãÕ$TåEôU„T5UD”ôâÀ¢&6U÷6VVG3Ô$4Uõ4TTE2Æ†VE÷6VVG3Ô„TEõ4TTE2Æ&ÓÔ$ÒÆ&—G3Ô$•E2À¢VW7F–öãÒ&g&÷¦VâÆV&æVBæV6W76—G’·F&vWBG&—fW2öæR&VÂ6VÆV7FVBÖf7B$UE$”UdRF†Vâ&V6Æ76–f–W27GVÂ×VÇF’ÖÖ—76–ær7FFR"À¢6†ævVCÒ&öffÆ–æR3ƒ‚F&vWB6VÆV7F–öâ6öææV7FVBFò7GVÂ3s"ô3s27V—6—F–öã²æòÆV&æVBvV–v‡G26†ævR"À¢–æ—F–Å÷öÆ–7“Ò&öæR6†&VBg&÷¦Vâ3ƒ&6Rf÷'v&BVÖ—G2æV6W76—G’æB†–FFVâ7FFW3²g&÷¦Vâ3ƒ‚†VB6VÆV7G2F&vWB"À¢÷7E÷öÆ–7“Ò&öæRg&÷¦Vâ3ƒæV6W76—G’ÖöæÇ’FV6—6–öâgFW"7GVÂFÖ—76–öã²æò6V6öæB7V—6—F–öâ"À¢Æ–÷WCÒ&÷&–v–æÂ3sBÆö6Âf7BÆ–÷WBöæÇ“²æò3ƒB&VæÖ–ær–çFW'fVçF–öâ–â3ƒ’"À¢6ö†÷'CÒ&ÆÃsc‚”ÄõBäTTE2&÷w2v—F‚Ö—76–æs"ó3²F—67&–Ö–æF–ærF&vWB7V'6WCS#‚&WF–æVB"À¢&Æö6·3Ó‚ÆW—6öFW3Ó3ƒ#BÆW—6öFW5÷W%ö&Æö6³Ósc‚ÆF—67&–Ö–æF–æu÷&÷w5÷W%ö&Æö6³ÓS#‚À¢6ö×ÆWF–öåö&—G3Ó"Ç6VÆV7F÷'3Ó’À¢6÷W&6Uöf–ÆW3Õ4õU$4U2À¢6÷W&6Uö6öçG&7CÒ&V–v‡B3ƒRÖf÷&ÖB6–ævÆRÖf7Bf–ÆW3²ÆV&æVBF&vWB6†ö÷6W2v†–6‚W†7BVæGö–çB—2&÷VæC²öæÇ’6VÆV7FVBf7BÖ’V&Æ—6‚"À¢F&vWE÷&WÆ•÷&÷w3ÓS“"Ç7FF–5ö&6UöfVGW&U÷&÷w3ÓS3BÇ7FF–5ö&6UöfVGW&Uöf÷'v&G3ÓbÀ¢Æ—fUö–æ—F–Åö&6U÷&÷w3Ó3ƒ#BÆÆ—fU÷÷7Eö&6U÷&÷w3Ò&ÖV7W&VBÃâã3ƒ#B"À¢Æ—fU÷F&vWE÷&÷w3Ó3ƒ#BÇF÷FÅö&6U÷&÷w5öÖƒÓcƒ“S"À¢&6Uö6†V6·ö–çEöÆöG3Ó2ÇF&vWEö6†V6·ö–çEöÆöG3Ó’À¢G&–æ–æsÓÆg&W6…÷6VVG3ÓÆÖ…ö7V—6—F–öç5÷W%öW—6öFSÓÆÖ…÷÷7EöFV6—6–öç3ÓÀ¢–FVÅ÷&VG3Ó3ƒ#BÆ–FVÅ÷V&Æ–6F–öç3Ó3ƒ#BÀ¢–æ—F–Å÷&W6÷W&6W3Ò&÷&–v–æÃ&–çFW&æÂóF7V—6—F–öç2÷7FWs²öæR6öÖ&–æVBÆV&æVBFV6—6–öâ6†&vVB&Vf÷&R–çWB"À¢W‡V7FVEöÆ—fUöf—'7CÒ#–çFW&æÂóF7V—6—F–öç2÷7FW‚"À¢W‡V7FVEöÆ—fU÷÷7CÒ&gFW"7F–öã¶F—7F6ƒ"·÷7FFV6—6–öãÓãv–çFW&æÂó67V—6—F–öç2÷7FW""À¢F&vWE÷FV6†W#Ò'66÷&–æröæÇ“¢3ƒ‚–æfÇVVçF–Â×F&vWB6WC²æWfW"öÆ–7’÷&÷f–FW"–çWB"À¢÷7E÷FV6†W#Ò'66÷&–æröæÇ“¢3sBÆöv–6ÂæV6W76—G’öâ7GVÂf–æÂf—6–&ÆRf7G2"À¢vFSÒ&ÆÃ—ƒ"&Æö6·2¦W&ò–æ—F–Â÷F&vWB÷&WÆ’÷÷7Bö6öçG&7BW'&÷'3²W†7BöæR&VB÷V&Æ–6F–öâV6ƒ²F&vWBÆöv—G2&WÆ’3ƒ‚ÃÓRÓb"À¢7GVÅöæWGv÷&µö6ÆÇ3ÓÆç7vW%övVæW&F–öãÓÇ&ööeö6†V6¶W%ö6ÆÇ3ÓÆ6÷&UöWf–FVæ6U÷w&—FW3ÓÀ¢&öGV7F–öå÷'VçF–ÖUöÖöF–f–VCÔfÇ6RÆvFUöUö6æF–FFSÔfÇ6RÀ¢÷WGWG3×6÷'FVB„õUEUE2’À¢Æ–Ö—G3Ò'6ÖRf÷W"&WVFVFÇ’–ç7V7FVBFWfVÆ÷ÖVçBw&÷W3¶öæR7V—6—F–öâöæÇ“¶f—†VB$UE$”UdR÷&÷f–FW#¶æò—FW&F—fRÆææ–ærÇ&VæÖ–ærÆÆæwVvRÆç7vW"÷&ööb÷"gVÆÂvFTR" ¤Ôä”dU5Eõ4„Ò#f666##fSv3FSFc“s36CV33CVCCF&–#f6#F#†SvcFV6cSCr  ¦FVb&V6†V6²†3ƒ…÷7VÖÖ'’Â¦&w2“ ¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3ƒ…ö×VÇF–Ö—76–æu÷F&vWE÷6VÆV7F–öâ2&Wf–÷W0¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3sUög&÷¦Vå÷&VF–7F–öåöVF—B2VF—@¢&WV—&R†ÆVâ†&w2“ÓÓBÂ%F†—'FVVâ&–÷"7VÖÖ&–W2æB&W÷6—F÷'’&ö÷B&WV—&VB"¢&ö÷CÖ&w5²ÓÐ¢ƒÇsBÇ–ç2Ç&÷FV7FVC×&Wf–÷W2ç&V6†V6²†&w5³ÒÂ¦&w5³¥Ò¢&WV—&R†VF—Bç6††3ƒ…÷7VÖÖ'’“ÓÕ$TåEõ4„Â$3ƒ‚7VÖÖ'’6†ævVB"¢&VçCÖVF—Bç&VEö§6öâ†3ƒ…÷7VÖÖ'’“²&Wf–÷W2çfÆ–FFU÷&W7VÇB‡&VçB¢&WV—&R‡&VçE²&6öÖÖ—E÷6†%ÓÓÕ$TåEôU„T5UD”ôâæB&VçE²'7FGW2%ÓÓÒ%52 ¢æB&Wf–÷W2ç6VÆV7F÷%övFR‡&VçE²'6VÆV7F÷%÷&W7VÇG2%ÒÇ&VçE²&g&WVVæ7•÷&VfW&Væ6R%Ò¢æB&VçE²'6÷W&6Uö&Æö'2%ÓÓ×–ç2Â%w&öær66WFVB3ƒ‚6÷W&6R÷&W7VÇB"¢&÷FV7FVE·7G"…F‚†3ƒ…÷7VÖÖ'’’ç&W6öÇfR‚’•ÓÕ$TåEõ4„¢f÷"–â&VçE²&'F–f7G2%Ó ¢cÖVF—Bç6fUö6†–ÆB…F‚†3ƒ…÷7VÖÖ'’’ç&W6öÇfR‚’ç&VçBÆ²&f–ÆR%Ò¢&WV—&R†bæ—5öf–ÆR‚’æBbç7FB‚’ç7E÷6—¦SÓÖ²'6W&–Æ—¦VEö'—FW2%ÒæBVF—Bç6††b“ÓÖ²'6†#Sb%ÒÀ¢$6†ævVB3ƒ‚'F–f7C¢"¶²&f–ÆR%Ò¢&÷FV7FVE·7G"†bç&W6öÇfR‚’•ÓÖ²'6†#Sb%Ð¢–ç3ÖF–7B‡–ç2¢f÷"æÖR–â&Wf–÷W2äõtã ¢–ç5¶æÖUÓÖVF—Bæv—B‡&ö÷BÂ'&Wb×'6R"Å$TåEôU„T5UD”ôâ²#¢"¶æÖR’æFV6öFR‚’ç7G&—‚¢ÆÇ–ç3ÖF–7B‡–ç2¢f÷"æÖR–âõtã ¢ÆÇ–ç5¶æÖUÓÖVF—Bæv—B‡&ö÷BÂ'&Wb×'6R"Â$„TC¢"¶æÖR’æFV6öFR‚’ç7G&—‚¢&÷FV7FVBçWFFR†VF—Bç&÷FV7E÷G&VUöf–ÆW2‡&ö÷BÆÆÇ–ç2’¢&WV—&R†ÆVâ‡–ç2“ÓÓræBÆVâ‡&÷FV7FVB“ÓÓ#S‚Â%6÷W&6R÷&÷FV7FVBVæ–öâG&–gB"¢&WV—&R†F–vW7B†Öæ–fW7B‚’“ÓÔÔä”dU5Eõ4„Â$Öæ–fW7BG&–gB"¢&WGW&â&VçBÇƒÇsBÇ–ç2Ç&÷FV7FV@ ¦FVb&Vw&W76–öåöÖöGVÆW2‡&ö÷B“ ¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3ƒ…ö×VÇF–Ö—76–æu÷F&vWE÷6VÆV7F–öâ2&Wf–÷W0¢æÖW3×&Wf–÷W2ç&Vw&W76–öåöÖöGVÆW2‡&ö÷B¢&WV—&R†ÆVâ†æÖW2“ÓÖÆVâ‡6WB†æÖW2’“ÓÓs2Â$†—7F÷&–6Â&Vw&W76–öâÆ—7BG&–gB"¢&WGW&âæÖW2µ²'FW7G5öÆÒçFW7E÷cUö3ƒ•öÆ—fUö×VÇF–Ö—76–æu÷F&vWB%Ð ¦FVbfÆ–FFU÷&W7VÇB‡“ ¢&WV—&R‡²&W‡W&–ÖVçEö–B%ÓÓÔU…U$”ÔTåEô”BæB²'7FvR%ÓÓÕ5DtP¢æB²&F–væ÷7F–5öW†V7WF–öå÷fÆ–B%Ò—2G'VRÂ%w&öærö–æ6ö×ÆWFR3ƒ’"¢&WV—&R‡²&W—6öFW2%ÓÓÓ3ƒ#BæBÆVâ‡²'&V6÷&G2%Ò“ÓÓ‚æBÆVâ‡²'6VÆV7F÷%÷&WÆ’%Ò“ÓÓ¢æB²&&6Uö6†V6·ö–çEöÆöG2%ÓÓÓ2æB²'F&vWEö6†V6·ö–çEöÆöG2%ÓÓÓ¢æB²'F&vWE÷&WÆ•÷&÷w2%ÓÓÓS“"æB²&Æ—fUö–æ—F–Å÷&÷w2%ÓÓÓ3ƒ#@¢æBÃ×²&Æ—fU÷÷7E÷&÷w2%ÓÃÓ3ƒ#@¢æB²'F÷FÅö&6U÷&÷w2%ÓÓÓS3B³3ƒ#B·²&Æ—fU÷÷7E÷&÷w2%Ð¢æB²'F÷FÅ÷F&vWE÷&÷w2%ÓÓÓS“"³3ƒ#@¢æBÆVâ‡²'6÷W&6Uö&Æö'2%Ò“ÓÓræBÆVâ‡²&–çWE÷6†#Sb%Ò“ÓÓ#S€¢æBÆVâ‡²&'F–f7G2%Ò“ÓÓ2æB¶²&f–ÆR%Òf÷"–â²&'F–f7G2%×ÓÓÔõUEUE2À¢%v÷&¶ÆöBö6÷fW&vRG&–gB"¢&WV—&R†ÆÂ‡¶µÓÓÓf÷"²–â‚&æWu÷G&–æ–ær"Â&g&W6…÷6VVG2"Â&æWGv÷&µö6ÆÇ2"Â&ç7vW%övVæW&F–öâ"À¢'&ööeö6†V6¶W%ö6ÆÇ2"Â&6÷&UöWf–FVæ6U÷w&—FW2"’¢æB²'&öGV7F–öå÷'VçF–ÖUöÖöF–f–VB%Ò—2fÇ6RæB²&vFUöUö6æF–FFR%Ò—2fÇ6RÀ¢%66÷RG&–gB"¢&WV—&R‡²&7GVÅöf–ÆU÷&VG2%ÓÓ×²'F÷FÇ2%Õ²'&÷f–FW%ö6ÆÇ2%ÓÓ×²'F÷FÇ2%Õ²'V&Æ–6F–öç2%ÒÀ¢$”ò66÷VçF–ærG&–gB"¢&WV—&R‡²'7FGW2%ÓÓÒ‚%52"–bvFR‡²'&V6÷&G2%ÒÇ²'6VÆV7F÷%÷&WÆ’%Ò’VÇ6R$d”Â"’Â$vFRG&–gB" ¦FVb'Vâ‚¢Â÷WGWEöF—"ÂW‡V7FVEö†VBÂ¢§&VçG2“ ¢g&öÒföÆEöÆÒçcR–×÷'B7G'V7GW&VEö7V—6—F–öåöÆ–fV7–6ÆR2Æ–fP¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3sEöÆV&æVEöæV6W76—G’23s@¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3sUög&÷¦Vå÷&VF–7F–öåöVF—B2VF—@¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3s…÷f—6–&ÆUöÆVeö&–æF–ær2&–æF–æp¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3s•÷6†&VEöw&‚2w&€¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3ƒ%ög&÷¦Våöf7E÷&VæÖ–ær2g&÷¦Và¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3ƒU÷6–ævÆUöÖ—76–æuö7V—6—F–öâ2G&—fW ¢g&öÒföÆEöÆÒçcUö&Væ6†Ö&·2–×÷'BvFUöUö3ƒ…ö×VÇF–Ö—76–æu÷F&vWE÷6VÆV7F–öâ2F&vW@¢&ö÷CÕF‚…õöf–ÆUõò’ç&W6öÇfR‚’ç&VçG5³%Ð¢&w3×GWÆR‡&VçG5¶â²%÷7VÖÖ'’%Òf÷"â–â$”õ%ôäÔU5³¥Ò’²‡&ö÷BÂ¢FVbwV&B‚“ ¢&WV—&R†VF—Bæv—B‡&ö÷BÂ'&Wb×'6R"Â$„TB"’æFV6öFR‚’ç7G&—‚“ÓÖW‡V7FVEö†VBÂ$„TBÖ—6ÖF6‚"¢&WV—&R†VF—Bæv—B‡&ö÷BÂ&'&æ6‚"Â"Ò×6†÷rÖ7W'&VçB"’æFV6öFR‚’ç7G&—‚“ÓÒ&fVB÷6gB×F&vWBÖÆ÷72"Â$'&æ6‚Ö—6ÖF6‚"¢&WV—&R†æ÷BVF—Bæv—B‡&ö÷BÂ'7FGW2"Â"Ò×÷&6VÆ–â"Â"Ò×VçG&6¶VBÖf–ÆW3Öæò"’ç7G&—‚’Â$F—'G’G&6¶VBG&VR"¢wV&B‚¢ƒ‚ÇƒÇsBÇ–ç2Ç&÷FV7FVC×&V6†V6²‡&VçG5²&3ƒ…÷7VÖÖ'’%ÒÂ¦&w2¢÷WCÕF‚†÷WGWEöF—"“¶÷WBæÖ¶F—"‡&VçG3ÕG'VRÆW†—7Eöö³ÔfÇ6R¢7F'FVC×F–ÖRçW&eö6÷VçFW"‚“¶'F–f7G3ÕµÓ·&V6÷&G3ÕµÓ·&WÆ“ÕµÐ¢FVb&V6÷&Eöf–ÆR†æÖR“ ¢cÖ÷WBöæÖS¶'F–f7G2æVæB†F–7B†f–ÆSÖæÖRÇ6†#ScÖVF—Bç6††b’Ç6W&–Æ—¦VEö'—FW3Öbç7FB‚’ç7E÷6—¦R’¢FVb6fR†æÖRÇfÇVR“ ¢†÷WBöæÖR’çw&—FUö'—FW2†&Æö"‡fÇVR’“·&V6÷&Eöf–ÆR†æÖR¢6fR‚&Æ—fR×F&vWB×Æâæ§6öâ"ÆF–7B†Öæ–fW7B‚’Ç6÷W&6Uö&Æö'3×–ç2’¢G'“ ¢&–çB‚%´3ƒ•ÒÆâf—†VC²g&÷¦VâÆV&æVBF&vWBG&—fW2W†7FÇ’öæR&VÂ$UE$”UdS²æò6V6öæB7V—6—F–öâ"ÆfÇW6ƒÕG'VR¢F÷&6‚ç6WEöçVÕ÷F‡&VG2ƒ"“·F÷&6‚çW6UöFWFW&Ö–æ—7F–5öÆv÷&—F†×2…G'VR¢FFÆÖWFFFÖVF—BæÆöEöFF…F‚‡&VçG5²&3sE÷7VÖÖ'’%Ò’ç&W6öÇfR‚’ç&VçBÇsB¢&uöÆÃ×F÷&6‚æg&öÕöçV×’†FF²&fVGW&W2%Òæ6÷’‚’¢fÆ–C×F&vWE÷FV6†W"†FF²&fVGW&W2%ÒÆFF²'FV×ÆFUö–G2%ÒÆÖWFFF¢òÅòÆWfgVÆÂÆÖ—72Ç&öf–ÆS×F&vWBæ6ö†÷'EöÖ6·2‡&uöÆÂÆFF²&Æ&VÇ2%ÒÆFF²'7Æ—Eö6öFW2%ÒÇfÆ–B¢gVÆÅö—ƒÖçæfÆFæöç¦W&ò†WfgVÆÂ¢&WV—&R†ÆVâ†gVÆÅö—‚“ÓÓsc‚æB&öf–ÆU²&WfÅöF—67&–Ö–æF–ær%ÓÓÓS#‚æB†FF²&Æ&VÇ2%Õ¶WfgVÆÅÓÓÓ’æÆÂ‚’À¢$3ƒ’6ö†÷'BG&–gB"¢&s×F÷&6‚æg&öÕöçV×’†FF²&fVGW&W2%Õ¶WfgVÆÅÒæ6÷’‚’¢fÆ–EögVÆÃ×fÆ–E¶WfgVÆÅÓ¶w&÷W3ÖFF²&w&÷W2%Õ¶WfgVÆÅÓ·F–G3ÖFF²'FV×ÆFUö–G2%Õ¶WfgVÆÅÐ¢2F—67&–Ö–æF–ær7V'6WB&VÆF—fRFòF†Rsc‚gVÆÂ&÷w2à¢f3×fÆ–EögVÆÂç7VÒƒ“¶ÓÖÖ—75¶WfgVÆÅÐ¢F—67&–Ö–æF–æsÒ‡f3ÆÒ¢&WV—&R†–çB†F—67&–Ö–æF–ærç7VÒ‚’“ÓÓS#‚Â$3ƒ’F—67&–Ö–æF–ær7V'6WBG&–gB"¢&VçEöF—#ÕF‚‡&VçG5²&3ƒ…÷7VÖÖ'’%Ò’ç&W6öÇfR‚’ç&Vç@¢6fVCÖÆöE÷&VçE÷&VF–7F–öç2‡&VçEöF—"ò'–Æ÷B×&VF–7F–öç2æç¢"¢&WV—&R†çæ'&•öWVÂ‡6fVE²'&÷uö–æF–6W2%ÒÆgVÆÅö—‚’Â$3ƒ‚&÷r–FVçF—G’G&–gB"¢3ƒöF—#ÕF‚‡&VçG5²&3ƒ÷7VÖÖ'’%Ò’ç&W6öÇfR‚’ç&Vç@¢f—G3×¶e²'6VVB%Ó¦bf÷"b–âƒ²&f—E÷&V6÷&G2%Ò–be²&&Ò%ÓÓÔ$×Ð¢6VÆV7F÷%÷6†×²‡%²&&6U÷6VVB%ÒÇ%²&†VE÷6VVB%Ò“§%²&†VE÷6†#Sb%Òf÷""–âƒ…²'6VÆV7F÷%÷&W7VÇG2%×Ð¢&WV—&R‡6WB†f—G2“Ó×6WB„$4Uõ4TTE2’æB6WB‡6VÆV7F÷%÷6†“Ó×²†"Æ‚’f÷""–â$4Uõ4TTE2f÷"‚–â„TEõ4TTE7ÒÀ¢$g&÷¦Vâ6†V6·ö–çB6÷fW&vRG&–gB"¢&6W3×·Ó¶†VG3×·Ó¶&6Uög×·Ó¶†VEög×·Ð¢f÷""–â$4Uõ4TTE3 ¢&6W5¶%ÓÖg&÷¦Vâç&W7F÷&Uö&&R†3ƒöF—"öb'&ö&R×¶'Ò×´$×ÒçB"Æ"Ä$ÒÆf—G5¶%Õ²&f–æÅ÷6†#Sb%Ò¢&6Uög¶%ÓÖw&‚æf–ævW'&–çB†&6W5¶%Ò¢f÷"‚–â„TEõ4TTE3 ¢†VG5¶"Æ…Ó×&W7F÷&U÷6VÆV7F÷"‡&VçEöF—"öb'6VÆV7F÷"×¶'Ò×¶‡ÒçB"Æ"Æ‚Ç6VÆV7F÷%÷6†¶"Æ…Ò¢†VEög¶"Æ…Ó×F&vWBæ†VEöf–ævW'&–çB††VG5¶"Æ…Ò¢2&WÆ’3ƒ‚66WFVBF&vWB&VF–7F–öç2&Vf÷&Rç’Æ—fRW—6öFRà¢7FF–5ö&6U÷&÷w3×7FF–5ö&6Uöf÷'v&G3×7FF–5ö&6Uö6VÆÇ3Ó ¢f÷"&’Æ"–âVçVÖW&FR„$4Uõ4TTE2“ ¢fVBÆÖWFW#×F&vWBæ6GW&Uöf7EöfVGW&W2†&6W5¶%ÒÆ&–æF–ærç&W&U÷—"‡&r•³ÒÇ&rÆ&F6ƒÔ$D4‚¢7FF–5ö&6U÷&÷w2³ÖÖWFW%²'&÷w2%Ó·7FF–5ö&6Uöf÷'v&G2³ÖÖWFW%²&f÷'v&Eö6ÆÇ2%Ó·7FF–5ö&6Uö6VÆÇ2³ÖÖWFW%²&6VÆÅö6ÆÇ2%Ð¢Væ¶æ÷vã×F&vWBæÖ—76–æuöÖ6²‡&r¢f÷"†’Æ‚–âVçVÖW&FR„„TEõ4TTE2“ ¢–GƒÖ&’£2¶†¢Ç¢Åó×F&vWBç&VF–7E÷6VÆV7F÷"††VG5¶"Æ…ÒÆfVBÇVæ¶æ÷vâÆ&F6ƒÔ$D4‚¢§£×¢æçV×’‚“·7×6fVE²'&VF–7F–öç2%Õ¶–G…Ó·7£×6fVE²&Æöv—G2%Õ¶–G…Ð¢f–æ—FS×Væ¶æ÷vâæçV×’‚¢FVÇFÖfÆöB†çæÖ‚†çæ'2‡§¥¶f–æ—FUÒ×7¥¶f–æ—FUÒ’’¢WÖ&ööÂ†çæ'&•öWVÂ‡æçV×’‚’Ç7’¢&WV—&R†WæBFVÇFÃÔDôÂÂ$66WFVB3ƒ‚6VÆV7F÷"&WÆ’G&–gB"¢&WÆ’æVæB†F–7B†&6U÷6VVCÖ"Æ†VE÷6VVCÖ‚Ç&VF–7F–öç5öWVÃÖWÆÖ…ö'5öÆöv—EöF–ffW&Væ6SÖFVÇF’¢&WV—&R‚‡7FF–5ö&6U÷&÷w2Ç7FF–5ö&6Uöf÷'v&G2Ç7FF–5ö&6Uö6VÆÇ2“ÓÒƒS3BÃbÃC"’Â%7FF–2&WÆ’v÷&¶ÆöBG&–gB"¢6fR‚'6VÆV7F÷"×&WÆ’æ§6öâ"Ç&WÆ’¢&–çB‚%´3ƒ•Òó2ÆÃS“"3ƒ‚F&vWB&VF–7F–öç2&WÆ–VBW†7FÇ“²sc‚Æ—fR6÷W&6R&÷w2f—†VB"ÆfÇW6ƒÕG'VR ¢†÷WBò'6÷W&6W2"’æÖ¶F—"‚¢&÷f–FW'3×·Ó¶VæGö–çG3×¶&—C§·Òf÷"&—B–â$•E7Ð¢f÷"&—B–â$•E3 ¢f÷"’Æf–B–âVçVÖW&FR†G&—fW"äd5Eô”E2“ ¢æÖSÖb'6÷W&6W2öf7B×¶—ÒÖ6ö×ÆWF–öâ×¶&—GÒæ§6öâ#¶&#×6÷W&6Uö'—FW2†’Æ&—B¢†÷WBöæÖR’çw&—FUö'—FW2†&"“·&V6÷&Eöf–ÆR†æÖR¢6#ÖÆ–fRå6÷W&6T&–æF–ær†b$3ƒRÖf—‡GW&R×¶—Ò×¶&—GÒ"Æ†6†Æ–"ç6†#Sb†&"’æ†W†F–vW7B‚’¢&÷f–FW#ÖÆ–fRäf–ÆU6æ6†÷E&÷f–FW"†÷WBöæÖRÇ6"“·&÷f–FW'5¶’Æ&—EÓ×&÷f–FW ¢VæGö–çG5¶&—EÕ¶f–EÓÖÆ–fRäVæGö–çB‡6"Ç&÷f–FW" ¢FVç6SÖF–7B†æV6W76—G•÷&VF–7F–öç3ÖçægVÆÂ‚ƒ’Ã"Ãsc‚Ã"’ÂÓÆGG—SÖçæ–çC‚’À¢æV6W76—G•öÆöv—G3Öçç¦W&÷2‚ƒ’Ã"Ãsc‚Ã"Ã"’ÆGG—SÖçæfÆöC3"’À¢F&vWE÷&VF–7F–öç3ÖçægVÆÂ‚ƒ’Ã"Ãsc‚’ÂÓÆGG—SÖçæ–çC‚’À¢F&vWEöÆöv—G3ÖçægVÆÂ‚ƒ’Ã"Ãsc‚ÃB’ÂÖçæ–æbÆGG—SÖçæfÆöC3"’À¢÷7EöÆ&VÇ3ÖçægVÆÂ‚ƒ’Ã"Ãsc‚’ÂÓÆGG—SÖçæ–çC‚’¢Æ—fUöÖWFW#ÖF–7B‡&÷w3ÓÆf÷'v&Eö6ÆÇ3ÓÆ6VÆÅö6ÆÇ3Ó“²Æ—fU÷÷7E÷&÷w3Ó ¢v—F‚w¦—æ÷Vâ†÷WBò&W—6öFR×G&6W2æ§6öæÂæw¢"Â'wB"ÆVæ6öF–æsÒ'WFbÓ‚"ÆæWvÆ–æSÒ%Æâ"’2G&6S ¢f÷"&’Æ"–âVçVÖW&FR„$4Uõ4TTE2“ ¢f÷"†’Æ‚–âVçVÖW&FR„„TEõ4TTE2“ ¢–GƒÖ&’£2¶†¢f÷"&—B–â$•E3 ¢f–Ww3ÖG&—fW"æÖ¶U÷f–Ww2‡&rÆgVÆÅö—‚ÆG&—fW"äÄ”õUE5³ÒÆb$3ƒ’Ö'¶'ÒÖ‡¶‡Ò×g¶&—GÒ"¢&Vf÷&U÷&VG3×7VÒ‡&÷f–FW'5¶’Æ&—EÒç&VG2f÷"’–â&ævRƒB’¢ö'6W'fVBÆ'&—2ÆÖWFW#×'Våö&Æö6²‡f–Ww2ÆVæGö–çG5¶&—EÒÆ&6W5¶%ÒÆ†VG5¶"Æ…Ò¢f÷"²–âÆ—fUöÖWFW#¢Æ—fUöÖWFW%¶µÒ³ÖÖWFW%¶µÐ¢Æ—fU÷÷7E÷&÷w2³×7VÒƒf÷""–âö'6W'fVB–bÆVâ‡%²'†6W2%Ò“ÓÓ"¢FVç6U²&æV6W76—G•÷&VF–7F–öç2%Õ¶–G‚Æ&—EÓÖ'&—5²&æV6W76—G•÷&VF–7F–öç2%Ð¢FVç6U²&æV6W76—G•öÆöv—G2%Õ¶–G‚Æ&—EÓÖ'&—5²&æV6W76—G•öÆöv—G2%Ð¢FVç6U²'F&vWE÷&VF–7F–öç2%Õ¶–G‚Æ&—EÓÖ'&—5²'F&vWE÷&VF–7F–öç2%Ð¢FVç6U²'F&vWEöÆöv—G2%Õ¶–G‚Æ&—EÓÖ'&—5²'F&vWEöÆöv—G2%Ð¢Væ¶æ÷vã×F&vWBæÖ—76–æuöÖ6²‡F÷&6‚æg&öÕöçV×’†FF²&fVGW&W2%Õ¶WfgVÆÅÒæ6÷’‚’’’æçV×’‚¢f–æ—FS×Væ¶æ÷và¢&VçEöÆöv—G3×6fVE²&Æöv—G2%Õ¶–G…Ð¢FVÇFÖfÆöB†çæÖ‚†çæ'2†'&—5²'F&vWEöÆöv—G2%Õ¶f–æ—FUÒ×&VçEöÆöv—G5¶f–æ—FUÒ’’¢66÷&W3ÕµÐ¢f÷"¢Â‡"ÇfÒÇF–B’–âVçVÖW&FR‡¦—†ö'6W'fVBÇfÆ–EögVÆÂÇF–G2Ç7G&–7CÕG'VR’“ ¢3Ö76W72‡"ÇfÒÆ–çB†gVÆÅö—…¶¥Ò’Æ–çB‡F–B’ÆÖWFFFÆ&—BÆ–çB‡6fVE²'&VF–7F–öç2%Õ¶–G‚Æ¥Ò’¢66÷&W2æVæB‡2“¶FVç6U²'÷7EöÆ&VÇ2%Õ¶–G‚Æ&—BÆ¥Ó×5²'÷7EöW‡V7FVB%Ð¢G&6Rçw&—FR†§6öâæGV×2†F–7B†&6U÷6VVCÖ"Æ†VE÷6VVCÖ‚Æ6ö×ÆWF–öãÖ&—BÀ¢6÷W&6U÷&÷sÖ–çB†gVÆÅö—…¶¥Ò’Ç66÷&S×2ÇG&6S×"’Ç6÷'Eö¶W—3ÕG'VRÀ¢6W&F÷'3Ò‚"Â"Â#¢"’ÆÆÆ÷uöæãÔfÇ6R’²%Æâ"¢F÷FÇ3×¶³§7VÒ‡5¶µÒf÷"2–â66÷&W2’f÷"²–â4õTåDU%7Ð¢7GVÅ÷&VG3×7VÒ‡&÷f–FW'5¶’Æ&—EÒç&VG2f÷"’–â&ævRƒB’’Ö&Vf÷&U÷&VG0¢&WV—&R†7GVÅ÷&VG3Ó×F÷FÇ5²'&÷f–FW%ö6ÆÇ2%ÒÂ%&÷f–FW"&VB66÷VçF–ærF—67&Wæ7’"¢&V3ÖF–7B†&6U÷6VVCÖ"Æ†VE÷6VVCÖ‚Æ6ö×ÆWF–öãÖ&—BÆW—6öFW3Ósc‚À¢F—67&–Ö–æF–æu÷&÷w3ÓS#‚À¢F—67&–Ö–æF–æu÷F&vWEöW'&÷'3×7VÒ‡66÷&W5¶¥Õ²'F&vWEöW'&÷"%Òf÷"¢–âçæfÆFæöç¦W&ò†F—67&–Ö–æF–ær’’À¢–æ—F–Å÷F&vWEöÖ…ö'5öÆöv—EöF–ffW&Væ6SÖFVÇFÀ¢÷7E÷7Vff–6–VçC×7VÒ‡5²'÷7EöW‡V7FVB%ÓÓÓf÷"2–â66÷&W2’À¢÷7EöæVVG3×7VÒ‡5²'÷7EöW‡V7FVB%ÓÓÓf÷"2–â66÷&W2’À¢'•öw&÷W×·7G"†r“§¶³§7VÒ‡66÷&W5¶¥Õ¶µÒf÷"¢–âçæfÆFæöç¦W&ò†w&÷W3ÓÖr’’f÷"²–â4õTåDU%7Ð¢f÷"r–â6÷'FVB‡6WB†w&÷W2çFöÆ—7B‚’’—ÒÀ¢¢§F÷FÇ2¢&V6÷&G2æVæB‡&V2¢&–çB†b%´3ƒ•Ò&Æö6³×¶ÆVâ‡&V6÷&G2—Òó‚&6S×¶'Ò†VC×¶‡Ò&—C×¶&—GÒ ¢b&f–ÆVC×·&V5²vf–ÆVBu×Ò÷7EöæVVG3×·&V5²w÷7EöæVVG2u×Ò&VG3×¶7GVÅ÷&VG7Ò"ÆfÇW6ƒÕG'VR¢&V6÷&Eöf–ÆR‚&W—6öFR×G&6W2æ§6öæÂæw¢"“·6fR‚&W—6öFR×&W7VÇG2æ§6öâ"Ç&V6÷&G2¢çç6fW¥ö6ö×&W76VB†÷WBò&W—6öFR×&VF–7F–öç2æç¢"Â¢¦FVç6RÇ&÷uö–æF–6W3ÖgVÆÅö—‚æ7G—R‚#Æ“B"’À¢&6U÷6VVG3Öçç&WVB†çæ6'&’„$4Uõ4TTE2ÆGG—SÒ#Æ“B"’Ã2’À¢†VE÷6VVG3ÖççF–ÆR†çæ6'&’„„TEõ4TTE2ÆGG—SÒ#Æ“B"’Ã2’¢&V6÷&Eöf–ÆR‚&W—6öFR×&VF–7F–öç2æç¢"¢&–çB‚%´3ƒ•Ò"ó2ÆÃ3ƒ#BÆ—fRW—6öFW26öÆÆV7FVC²6VÆV7FVBf7BöæÇ“²æò6V6öæB7V—6—F–öâ"ÆfÇW6ƒÕG'VR ¢wV&B‚“·&V6†V6²‡&VçG5²&3ƒ…÷7VÖÖ'’%ÒÂ¦&w2¢&WV—&R…¶w&‚æf–ævW'&–çB†&6W5¶%Ò’f÷""–â$4Uõ4TTE5ÓÓÕ¶&6Uög¶%Òf÷""–â$4Uõ4TTE5ÒÀ¢$g&÷¦Vâ3ƒ&6R6†ævVB"¢&WV—&R…·F&vWBæ†VEöf–ævW'&–çB††VG5¶"Æ…Ò’f÷""–â$4Uõ4TTE2f÷"‚–â„TEõ4TTE5ÒÓÐ¢¶†VEög¶"Æ…Òf÷""–â$4Uõ4TTE2f÷"‚–â„TEõ4TTE5ÒÂ$g&÷¦Vâ3ƒ‚†VB6†ævVB"¢f÷"bÆ‚–â&÷FV7FVBæ—FV×2‚“§&WV—&R†VF—Bç6††b“ÓÖ‚Â%&÷FV7FVB–çWB6†ævVC¢"¶b¢f÷"–â'F–f7G3§&WV—&R†VF—Bç6††÷WBö²&f–ÆR%Ò“ÓÖ²'6†#Sb%ÒÂ$÷WGWB6†ævVC¢"¶²&f–ÆR%Ò¢F÷FÇ3×¶³§7VÒ‡%¶µÒf÷""–â&V6÷&G2’f÷"²–â4õTåDU%7Ð¢&VG3×7VÒ‡ç&VG2f÷"–â&÷f–FW'2çfÇVW2‚’“·&VF'—FW3×7VÒ‡æ'—FW5÷&VBf÷"–â&÷f–FW'2çfÇVW2‚’¢&WV—&R‡&VG3Ó×F÷FÇ5²'&÷f–FW%ö6ÆÇ2%ÒÂ%F÷FÂ&÷f–FW"”òG&–gB"¢&W7VÇCÖF–7B†W‡W&–ÖVçEö–CÔU…U$”ÔTåEô”BÇ7FvSÕ5DtRÆ6öÖÖ—E÷6†ÖW‡V7FVEö†VBÀ¢7FGW3Ò%52"–bvFR‡&V6÷&G2Ç&WÆ’’VÇ6R$d”Â"ÆF–væ÷7F–5öW†V7WF–öå÷fÆ–CÕG'VRÀ¢3ƒ…÷7VÖÖ'•÷6†#ScÕ$TåEõ4„Ç6÷W&6Uö&Æö'3×–ç2Æ–çWE÷6†#Sc×&÷FV7FVBÆ'F–f7G3Ö'F–f7G2À¢6VÆV7F÷%÷&WÆ“×&WÆ’Ç&V6÷&G3×&V6÷&G2ÇF÷FÇ3×F÷FÇ2ÆW—6öFW3Ó3ƒ#BÀ¢F&vWE÷&WÆ•÷&÷w3ÓS“"Ç7FF–5ö&6UöfVGW&U÷&÷w3ÓS3BÇ7FF–5ö&6UöfVGW&Uöf÷'v&G3ÓbÀ¢Æ—fUö–æ—F–Å÷&÷w3Ó3ƒ#BÆÆ—fU÷÷7E÷&÷w3ÖÆ—fU÷÷7E÷&÷w2À¢F÷FÅö&6U÷&÷w3ÓS3B¶Æ—fUöÖWFW%²'&÷w2%ÒÇF÷FÅ÷F&vWE÷&÷w3ÓS“"³3ƒ#BÀ¢Æ—fUö–æfW&Væ6Uöf÷'v&Eö6ÆÇ3ÖÆ—fUöÖWFW%²&f÷'v&Eö6ÆÇ2%ÒÆÆ—fUö–æfW&Væ6Uö6VÆÅö6ÆÇ3ÖÆ—fUöÖWFW%²&6VÆÅö6ÆÇ2%ÒÀ¢&6Uö6†V6·ö–çEöÆöG3Ó2ÇF&vWEö6†V6·ö–çEöÆöG3Ó’À¢7GVÅö7V—6—F–öç3×F÷FÇ5²'&÷f–FW%ö6ÆÇ2%ÒÆ7GVÅöf–ÆU÷&VG3×&VG2À¢&÷f–FW%ö'—FW5÷&VC×&VF'—FW2ÇF6·f–Wuöf7E÷V&Æ–6F–öç3×F÷FÇ5²'V&Æ–6F–öç2%ÒÀ¢æWu÷G&–æ–æsÓÆg&W6…÷6VVG3ÓÆæWGv÷&µö6ÆÇ3ÓÆç7vW%övVæW&F–öãÓÇ&ööeö6†V6¶W%ö6ÆÇ3ÓÀ¢6÷&UöWf–FVæ6U÷w&—FW3ÓÇ&öGV7F–öå÷'VçF–ÖUöÖöF–f–VCÔfÇ6RÆvFUöUö6æF–FFSÔfÇ6RÀ¢Vçf—&öæÖVçCÖF–7B‡F÷&6ƒ×F÷&6‚åõ÷fW'6–öåõòÆçV×“Öçåõ÷fW'6–öåõòÆFWf–6SÒ&7R"ÆGG—SÒ&fÆöC3""ÇF‡&VG3Ó"’À¢vÆÅö6Æö6µ÷6V6öæG3×F–ÖRçW&eö6÷VçFW"‚’×7F'FVBÀ¢Æ–Ö—FF–öç3Õ²'6ÖRf÷W"&WVFVFÇ’–ç7V7FVBFWfVÆ÷ÖVçBw&÷W3¶æ÷B–æFWVæFVçBf–æÂ6öæf—&ÖF–öâ"À¢&öæR7V—6—F–öâÖ†–×VÓ·÷7BäTTE2æWfW"G&–vvW'26V6öæBF&vWBö7F–öâ"À¢&f—†VB$UE$”UdRæBöæRÆö6Âf–ÆR&÷f–FW#·FööÂ÷&÷f–FW"6†ö–6R&VÖ–ç2†æGw&—GFVâ"À¢&–FVçF—G’ö÷&–v–æÂ3sBÆö6ÂÆ–÷WBöæÇ“´3ƒBô3ƒR&VæÖ–ærF‚æ÷B&WFW7FVB"À¢'F&vWBæB÷7BÆöv–6ÂFV6†W'2&R66÷&–æröæÇ“¶æòç7vW"÷&ööböÆæwVvRöÆ&vW"W‡&W76–öç2%Ò¢fÆ–FFU÷&W7VÇB‡&W7VÇB“²†÷WBò'7VÖÖ'’æ§6öâ"’çw&—FUö'—FW2†&Æö"‡&W7VÇB’¢&–çB‚%´3ƒ•Ò2ó26÷W&6Rö÷WGWB&W6W'fF–öâ6†V6¶VB"ÆfÇW6ƒÕG'VR¢&–çB‚#ÓÓÒ3ƒ’$U5TÅBÓÓÒ"ÆfÇW6ƒÕG'VR“·&–çB†&Æö"‡&W7VÇB’æFV6öFR‚’ÆfÇW6ƒÕG'VR¢&WGW&â&W7VÇ@¢W†6WBW†6WF–öâ2W†3 ¢†÷WBò&–çfÆ–Bæ§6öâ"’çw&—FUö'—FW2†&Æö"†F–7B†W‡W&–ÖVçEö–CÔU…U$”ÔTåEô”BÇ7FGW3Ò$”ådÄ”B"À¢F–væ÷7F–5öW†V7WF–öå÷fÆ–CÔfÇ6RÆW'&÷#×7G"†W†2’Æ6ö×ÆWFVE÷&V6÷&G3×&V6÷&G2Æ6ö×ÆWFVE÷&WÆ“×&WÆ’’’¢&—6P ¦FVbÖ–â‚“ ¢Ö&w'6Rä&wVÖVçE'6W"†FW67&—F–öãÕõöFö5õò¢f÷"â–â$”õ%ôäÔU3 ¢æFEö&wVÖVçB‚"ÒÒ"¶â²"×7VÖÖ'’"ÇG—SÕF‚Ç&WV—&VCÕG'VR¢æFEö&wVÖVçB‚"ÒÖ÷WGWBÖF—""ÇG—SÕF‚Ç&WV—&VCÕG'VR“·æFEö&wVÖVçB‚"ÒÖW‡V7FVBÖ†VB"Ç&WV—&VCÕG'VR¢'Vâ‚¢§f'2‡ç'6Uö&w2‚’’ ¦–bõöæÖUõóÓÒ%õöÖ–åõò# ¢Ö–â‚