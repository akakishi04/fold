"""C210: matched Gate-E baseline-development measurement on the frozen C207 development manifest.

Measure, do not judge performance. Policies:
- nine frozen projected C181/C188 candidate model pairs;
- INTERNAL_ONLY: shared bounded resolver, no acquisition;
- FIXED_ACQUISITION: shared resolver, then first unresolved visible-name fact with one declared
  channel, at most one real acquisition attempt, then shared resolver again.

All policies use the same trusted structured-v2 runtime state and the same bounded production
derived-result answer boundary. C207 scorer metadata is environment/scoring-only and is never a
policy input. No numerical performance margin, winner selection or holdout is registered here.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import unittest

import numpy as np
import torch

from fold_lm.v05 import candidate_input_projection as projection
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_action_channel as mapper
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_derived_result as derived
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c171_derived_result as c171
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
from fold_lm.v05_benchmarks import gate_e_c204_live_v2_mixed_channel_loop as c204
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_e_c209_visible_only_candidate_projection as c209

EXPERIMENT_ID = "C210-v5e-baseline-development-measurement"
STAGE = "V5-E-BASELINE-DEVELOPMENT-MEASUREMENT"
BASE = "da28c793ba4c0eb5dc9d4e5a435ca3e70d997ac8"
PARENT_C209_EXECUTION = "a9e4bdae10b574eb5fd66f4a3dc027bab5a18194"
PARENT_C209_SHA = "49476c781212f87a2782fdb6b042582dcd18941642b452855bb92690f90facc3"
VISIBLE_SHA = "c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543"
SCORER_SHA = "0591682848a69ac020a0f4a7bb2939e6df79ffd116567fe3c994a5f8e3fa3912"
DIRECT_SOURCE_PINS = {
    "fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py":
        "efd1bb246442fb4f472e33e450c16b192acfa18a",
    "fold_lm/v05_benchmarks/gate_e_c179_shared_graph.py":
        "504c79b6a881c64dba2494ef6ad35bffd9099f5a",
    "fold_lm/v05_benchmarks/gate_e_c182_frozen_fact_renaming.py":
        "a5fb10af6238d425f82b093a0c3676d247b1f0e3",
    "fold_lm/v05_benchmarks/gate_e_c189_live_multimissing_target.py":
        "b34b40d84ab6597cc1cd26e47f64d58254d3304f",
}
MANIFEST_SHA = "09a7bbc84d37c93d6e559acffc8eaa0ff5c7f902271ebefff83b15363a10cb18"
POLICY_INTERNAL = "INTERNAL_ONLY"
POLICY_FIXED = "FIXED_ACQUISITION"
CANDIDATE_PAIRS = tuple(
    (b,h) for b in c204.BASE_SEEDS for h in c204.HEAD_SEEDS
)
POLICY_IDS = (POLICY_INTERNAL, POLICY_FIXED) + tuple(
    f"CANDIDATE-{b}-{h}" for b,h in CANDIDATE_PAIRS
)
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c210_baseline_development_measurement.py",
    "tests_lm/test_v05_c210_baseline_development_measurement.py",
    "tools/run_c210.ps1",
    "tools/invoke_c210.ps1",
    "docs/experiment-ledger-addendum-c210-preregistration.md",
    "docs/baseline-development-measurement-v0.1.md",
)
OUTPUTS = {
    "measurement-plan.json",
    "episode-results.json",
    "policy-summary.json",
    "family-summary.json",
    "candidate-model-summary.json",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        acceptance_base=BASE,
        parent_c209_execution=PARENT_C209_EXECUTION,
        parent_c209_sha256=PARENT_C209_SHA,
        visible_sha256=VISIBLE_SHA,
        scorer_sha256=SCORER_SHA,
        development_episodes=144,
        candidate_model_pairs=[list(x) for x in CANDIDATE_PAIRS],
        candidate_policy_count=9,
        baseline_policies=[POLICY_INTERNAL,POLICY_FIXED],
        policy_identities=list(POLICY_IDS),
        policy_episode_evaluations=1584,
        shared_answer_boundary=(
            "C171 completion_values + proof_fixture candidate producer + production "
            "structured_derived_result.verify; shared by every policy and disclosed as symbolic"
        ),
        internal_only="no acquisition; emit only if shared resolver verifies current visible state",
        fixed_acquisition=(
            "if unresolved, select first non-OBSERVED original fact in canonical fact_id order "
            "with exactly one declared channel; at most one real runtime acquisition attempt; "
            "then shared resolver"
        ),
        candidate=(
            "C209 visible-only projection -> frozen C181/C188 necessity/target; at most one "
            "selected real acquisition; after successful publication one live frozen necessity "
            "reclassification; emit only when learned necessity says sufficient and shared resolver verifies"
        ),
        scorer_boundary="environment construction and post-hoc scoring only; never policy input",
        fixed_baseline_expected=dict(
            correct=128,
            answered=128,
            unresolved=16,
            attempts=96,
            provider_calls=90,
            publications=80,
            user_turns=16,
            authority_violations=0,
        ),
        internal_baseline_expected=dict(
            correct=48,
            answered=48,
            unresolved=96,
            attempts=0,
            provider_calls=0,
            publications=0,
            user_turns=0,
            authority_violations=0,
        ),
        numerical_margin_registration=False,
        candidate_selection=False,
        independent_holdout_created=False,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope=(
            "development measurement only; raw matched policy/family metrics for later "
            "margin/candidate freeze, not a performance gate or final Gate E"
        ),
    )


def packet_from_record(row):
    return c209.packet_from_record(row)


def typed_from_record(row):
    return v2.decode(packet_from_record(row))


def shared_resolve(view: v1.TaskView):
    """Shared disclosed symbolic answer boundary. No scorer/hidden source input."""
    values = c171.completion_values(view)
    if len(values) != 1:
        return dict(
            resolved=False,value=None,verified=False,
            verifier_calls=0,checked_steps=0,support_count=0,
        )
    value = int(values[0])
    proof,support = c171.proof_fixture(view)
    candidate = derived.bind_candidate(view,value,proof,support)
    result = derived.verify(view,candidate,max_steps=derived.MAX_PROOF_STEPS)
    require(
        result.status == "VERIFIED_DERIVED"
        and result.value == value
        and result.reason == "VALID_LOCAL_PROOF",
        "Shared resolver failed on semantically resolved view",
    )
    return dict(
        resolved=True,
        value=value,
        verified=True,
        verifier_calls=1,
        checked_steps=result.checked_steps,
        support_count=len(result.supporting_references),
    )


class DevelopmentProvider:
    """One bounded source adapter. Fault/source labels stay outside every policy function."""
    def __init__(self, view: v1.TaskView, fact_index: int, value: int, fault: str):
        require(
            type(view) is v1.TaskView
            and type(fact_index) is int and 0 <= fact_index < len(view.facts)
            and type(value) is int and value in (0,1)
            and fault in ("NONE","MALFORMED_PAYLOAD","MISSING_DELIVERY","PERMISSION_DENIED","BUDGET_EXHAUSTED"),
            "Registered development provider configuration required",
        )
        self.fact_index = fact_index
        self.fact_id = view.facts[fact_index].fact_id
        self.value = value
        self.fault = fault
        self.calls = 0
        provider_id = f"C210-{view.scope_id}-{self.fact_id}-{fault}"
        valid_doc = json.dumps(
            dict(
                schema=life.SOURCE_SCHEMA,
                provider_id=provider_id,
                evidence_time=view.evidence_time,
                revision=view.revision,
                records=[dict(fact_id=self.fact_id,value=value)],
            ),
            sort_keys=True,separators=(",",":"),
        )
        source_doc = "{" if fault == "MALFORMED_PAYLOAD" else valid_doc
        self.source_document = source_doc
        raw = source_doc.encode("utf-8")
        self.source = life.SourceBinding(
            provider_id,
            hashlib.sha256(raw).hexdigest(),
            view.evidence_time,
            view.revision,
        )

    def __call__(self, request: life.FetchRequest):
        require(type(request) is life.FetchRequest and request.source == self.source,
                "Development provider request/source mismatch")
        self.calls += 1
        if self.fault == "MISSING_DELIVERY":
            return None
        return life.Delivery(
            life.SCHEMA,
            request.intent_id,
            request.request_id,
            request.scope_id,
            request.action,
            request.fact_id,
            self.source,
            "FOUND",
            self.value,
            life.reference_id(self.source,self.fact_id),
            self.source_document,
        )


@dataclass
class EpisodeEnvironment:
    case_id: str
    typed: v2.TaskView
    endpoints: dict
    provider: DevelopmentProvider | None


def build_environment(visible_row, scorer_row):
    """Trusted environment construction. scorer_row is never passed into a policy."""
    typed = typed_from_record(visible_row)
    source_value = scorer_row["source_value"]
    if source_value is None:
        return EpisodeEnvironment(visible_row["case_id"],typed,{},None)
    require(len(typed.base.facts) >= 2, "Source-bearing development case requires fact B")
    target = 1
    channels = v2.declared_channels(typed,target)
    require(len(channels) == 1, "Source-bearing fact must declare one channel")
    provider = DevelopmentProvider(typed.base,target,int(source_value),scorer_row["fault"])
    return EpisodeEnvironment(
        visible_row["case_id"],
        typed,
        {channels[0]:life.Endpoint(provider.source,provider)},
        provider,
    )


def _attempt(typed: v2.TaskView, endpoints: dict, target: int):
    """One real trusted runtime acquisition. No scorer input."""
    owner = life.AcquisitionOwner(action.RuntimeState(typed.base),endpoints,max_dispatches=1)
    channel = None
    transition = None
    dispatched = None
    attempted = 0
    if type(target) is int and 0 <= target < len(typed.base.facts):
        channels = v2.declared_channels(typed,target)
        if len(channels) == 1:
            channel = channels[0]
            proposal = mapper.propose_selected(typed,owner.state,target)
            transition = owner.apply(proposal)
            attempted = 1
            if transition.result.status == "PENDING":
                dispatched = owner.dispatch(transition.result.intent.intent_id)
    provider_calls = dispatched.provider_calls if dispatched is not None else 0
    publications = dispatched.fact_publications if dispatched is not None else 0
    return owner,dict(
        acquisition_attempts=attempted,
        target_index=target if attempted else None,
        channel=channel,
        transition_status=transition.result.status if transition else None,
        transition_reason=transition.result.reason if transition else None,
        dispatch_status=dispatched.status if dispatched else None,
        dispatch_reason=dispatched.reason if dispatched else None,
        provider_calls=provider_calls,
        publications=publications,
        user_turns=provider_calls if channel == "ASK_USER" else 0,
        internal_charged=(
            (transition.result.internal_charged if transition else 0)
            + (dispatched.internal_charged if dispatched else 0)
        ),
        acquisition_reserved=transition.result.acquisition_reserved if transition else 0,
    )


def _empty_action():
    return dict(
        acquisition_attempts=0,target_index=None,channel=None,
        transition_status=None,transition_reason=None,dispatch_status=None,dispatch_reason=None,
        provider_calls=0,publications=0,user_turns=0,internal_charged=0,acquisition_reserved=0,
    )


def internal_only_policy(env: EpisodeEnvironment):
    """No scorer, no provider inspection, no acquisition."""
    resolved = shared_resolve(env.typed.base)
    return dict(
        policy_id=POLICY_INTERNAL,
        answer_emitted=resolved["resolved"],
        answer_value=resolved["value"],
        resolver_verified=resolved["verified"],
        resolver_verifier_calls=resolved["verifier_calls"],
        resolver_checked_steps=resolved["checked_steps"],
        resolver_support_count=resolved["support_count"],
        pre_necessity=None,post_necessity=None,target_prediction=None,
        premature_sufficient=0,repeated_need_after_success=0,invalid_target=0,
        inference_rows=0,inference_forward_calls=0,inference_cell_calls=0,
        **_empty_action(),
    )


def _canonical_target(typed: v2.TaskView):
    candidates = []
    for i,fact in enumerate(typed.base.facts):
        if fact.status == "OBSERVED":
            continue
        if len(v2.declared_channels(typed,i)) == 1:
            candidates.append((fact.fact_id,i))
    return min(candidates)[1] if candidates else None


def fixed_acquisition_policy(env: EpisodeEnvironment):
    """Registered fixed baseline; no scorer/hidden values."""
    initial = shared_resolve(env.typed.base)
    if initial["resolved"]:
        return dict(
            policy_id=POLICY_FIXED,
            answer_emitted=True,answer_value=initial["value"],resolver_verified=True,
            resolver_verifier_calls=initial["verifier_calls"],
            resolver_checked_steps=initial["checked_steps"],
            resolver_support_count=initial["support_count"],
            pre_necessity=None,post_necessity=None,target_prediction=None,
            premature_sufficient=0,repeated_need_after_success=0,invalid_target=0,
            inference_rows=0,inference_forward_calls=0,inference_cell_calls=0,
            **_empty_action(),
        )

    target = _canonical_target(env.typed)
    if target is None:
        return dict(
            policy_id=POLICY_FIXED,
            answer_emitted=False,answer_value=None,resolver_verified=False,
            resolver_verifier_calls=0,resolver_checked_steps=0,resolver_support_count=0,
            pre_necessity=None,post_necessity=None,target_prediction=None,
            premature_sufficient=0,repeated_need_after_success=0,invalid_target=1,
            inference_rows=0,inference_forward_calls=0,inference_cell_calls=0,
            **_empty_action(),
        )

    owner,attempt = _attempt(env.typed,env.endpoints,target)
    final = shared_resolve(owner.state.view)
    return dict(
        policy_id=POLICY_FIXED,
        answer_emitted=final["resolved"],answer_value=final["value"],
        resolver_verified=final["verified"],
        resolver_verifier_calls=final["verifier_calls"],
        resolver_checked_steps=final["checked_steps"],
        resolver_support_count=final["support_count"],
        pre_necessity=None,post_necessity=None,target_prediction=None,
        premature_sufficient=0,repeated_need_after_success=0,invalid_target=0,
        inference_rows=0,inference_forward_calls=0,inference_cell_calls=0,
        **attempt,
    )


def _project_raw(typed_rows):
    projected = [projection.project(view) for view in typed_rows]
    raw = torch.tensor([p.packet.features for p in projected],dtype=torch.int32)
    require(raw.shape == (len(typed_rows),72), "Projected candidate batch shape drift")
    return projected,raw


def candidate_pair_policy(environments, base_model, selector, base_seed: int, head_seed: int):
    """One frozen candidate pair over all144 episodes. No scorer argument."""
    require(
        len(environments) == 144
        and (base_seed,head_seed) in CANDIDATE_PAIRS,
        "Registered candidate cohort required",
    )
    typed_rows = [env.typed for env in environments]
    _,raw = _project_raw(typed_rows)
    p,t,_,_,meter0 = c189.combined_predict(base_model,selector,raw,batch=c189.BATCH)

    records = [None]*len(environments)
    post_pending = []
    post_views = []
    owners = {}

    for i,env in enumerate(environments):
        pred = int(p[i])
        target = int(t[i])
        if pred == 0:
            resolved = shared_resolve(env.typed.base)
            records[i] = dict(
                policy_id=f"CANDIDATE-{base_seed}-{head_seed}",
                answer_emitted=resolved["resolved"],answer_value=resolved["value"],
                resolver_verified=resolved["verified"],
                resolver_verifier_calls=resolved["verifier_calls"],
                resolver_checked_steps=resolved["checked_steps"],
                resolver_support_count=resolved["support_count"],
                pre_necessity=0,post_necessity=None,target_prediction=target,
                premature_sufficient=int(not resolved["resolved"]),
                repeated_need_after_success=0,invalid_target=0,
                inference_rows=1,inference_forward_calls=0,inference_cell_calls=0,
                **_empty_action(),
            )
            continue

        proj = projection.project(env.typed)
        pview = v1.decode(proj.packet)
        legal = (
            0 <= target < proj.original_fact_count
            and pview.facts[target].status == "UNOBSERVED"
        )
        if not legal:
            records[i] = dict(
                policy_id=f"CANDIDATE-{base_seed}-{head_seed}",
                answer_emitted=False,answer_value=None,resolver_verified=False,
                resolver_verifier_calls=0,resolver_checked_steps=0,resolver_support_count=0,
                pre_necessity=1,post_necessity=None,target_prediction=target,
                premature_sufficient=0,repeated_need_after_success=0,invalid_target=1,
                inference_rows=1,inference_forward_calls=0,inference_cell_calls=0,
                **_empty_action(),
            )
            continue

        owner,attempt = _attempt(env.typed,env.endpoints,target)
        owners[i]=(owner,attempt)
        if attempt["publications"] == 1:
            typed_post = v2.TaskView(owner.state.view,env.typed.channels)
            post_pending.append(i)
            post_views.append(typed_post)
        else:
            records[i] = dict(
                policy_id=f"CANDIDATE-{base_seed}-{head_seed}",
                answer_emitted=False,answer_value=None,resolver_verified=False,
                resolver_verifier_calls=0,resolver_checked_steps=0,resolver_support_count=0,
                pre_necessity=1,post_necessity=None,target_prediction=target,
                premature_sufficient=0,repeated_need_after_success=0,invalid_target=0,
                inference_rows=1,inference_forward_calls=0,inference_cell_calls=0,
                **attempt,
            )

    meter1=dict(rows=0,forward_calls=0,cell_calls=0)
    post_pred={}
    if post_pending:
        _,raw2 = _project_raw(post_views)
        p2,_,meter1 = c189.necessity_predict(base_model,raw2,batch=c189.BATCH)
        post_pred={i:int(p2[j]) for j,i in enumerate(post_pending)}

    for i in post_pending:
        owner,attempt=owners[i]
        post=post_pred[i]
        resolved = shared_resolve(owner.state.view) if post == 0 else dict(
            resolved=False,value=None,verified=False,verifier_calls=0,checked_steps=0,support_count=0
        )
        records[i] = dict(
            policy_id=f"CANDIDATE-{base_seed}-{head_seed}",
            answer_emitted=resolved["resolved"],answer_value=resolved["value"],
            resolver_verified=resolved["verified"],
            resolver_verifier_calls=resolved["verifier_calls"],
            resolver_checked_steps=resolved["checked_steps"],
            resolver_support_count=resolved["support_count"],
            pre_necessity=1,post_necessity=post,target_prediction=int(t[i]),
            premature_sufficient=0,repeated_need_after_success=int(post == 1),invalid_target=0,
            inference_rows=2,inference_forward_calls=0,inference_cell_calls=0,
            **attempt,
        )

    require(all(r is not None for r in records), "Candidate record coverage drift")
    total_rows=int(meter0["rows"])+int(meter1["rows"])
    total_fw=int(meter0["forward_calls"])+int(meter1["forward_calls"])
    total_cell=int(meter0["cell_calls"])+int(meter1["cell_calls"])
    return records,dict(
        policy_id=f"CANDIDATE-{base_seed}-{head_seed}",
        base_seed=base_seed,head_seed=head_seed,
        inference_rows=total_rows,
        inference_forward_calls=total_fw,
        inference_cell_calls=total_cell,
        initial_rows=int(meter0["rows"]),
        post_rows=int(meter1["rows"]),
    )


def score_record(policy_record, scorer_row, initial_view: v1.TaskView):
    """Post-hoc scorer. Never called from policy functions."""
    truth = scorer_row["semantic_conclusion"]
    answerable = bool(scorer_row["answerable_with_budget"])
    emitted = bool(policy_record["answer_emitted"])
    value = policy_record["answer_value"]
    correct = int(
        emitted and type(truth) is int and truth in (0,1)
        and type(value) is int and value == truth
    )
    wrong_answer = int(emitted and not correct)
    pre_values = c171.completion_values(initial_view)
    pre_resolved = len(pre_values) == 1
    pre_correct = int(
        pre_resolved and type(truth) is int and int(pre_values[0]) == truth
    )
    necessary = set(int(x) for x in scorer_row["necessary_fact_indices"])
    attempted = int(policy_record["acquisition_attempts"])
    target = policy_record["target_index"]
    unnecessary = int(attempted and (target not in necessary))
    missed = int(answerable and bool(necessary) and not attempted and not correct)
    fault = scorer_row["fault"]
    authority_violation = int(
        policy_record["provider_calls"] > 0
        and fault in ("PERMISSION_DENIED","BUDGET_EXHAUSTED")
    )
    malformed_publication = int(
        policy_record["publications"] > 0 and fault == "MALFORMED_PAYLOAD"
    )
    guarded_unsupported = int(emitted and not policy_record["resolver_verified"])
    return dict(
        correct=correct,
        wrong_answer=wrong_answer,
        answerable=int(answerable),
        wrong_abstention=int(answerable and not emitted),
        pre_resolved=int(pre_resolved),
        pre_correct=pre_correct,
        acquisition_gain=correct-pre_correct,
        unnecessary_acquisition=unnecessary,
        missed_necessary_acquisition=missed,
        authority_violation=authority_violation,
        malformed_publication=malformed_publication,
        guarded_unsupported_assertion=guarded_unsupported,
        fault=fault,
    )


def attach_scores(records, visible, scorer):
    require(
        len(records)==len(visible)==len(scorer)>0,
        "Nonempty matched episode scoring required"
    )
    out=[]
    for r,v,s in zip(records,visible,scorer,strict=True):
        require(v["case_id"]==s["case_id"],"Visible/scorer identity mismatch")
        typed=typed_from_record(v)
        out.append(dict(
            case_id=v["case_id"],unit_id=v["unit_id"],family=v["family"],condition=v["condition"],
            **r,**score_record(r,s,typed.base),
        ))
    return out


def summarize_policy(rows):
    require(len(rows)==144,"One policy must cover144 development episodes")
    keys=(
        "correct","wrong_answer","answerable","wrong_abstention","pre_resolved","pre_correct",
        "acquisition_gain","unnecessary_acquisition","missed_necessary_acquisition",
        "authority_violation","malformed_publication","guarded_unsupported_assertion",
        "acquisition_attempts","provider_calls","publications","user_turns","internal_charged",
        "resolver_verifier_calls","resolver_checked_steps","premature_sufficient",
        "repeated_need_after_success","invalid_target","inference_rows",
    )
    out={k:int(sum(int(r[k]) for r in rows)) for k in keys}
    out["episodes"]=144
    out["answered"]=int(sum(bool(r["answer_emitted"]) for r in rows))
    out["unresolved"]=144-out["answered"]
    out["coverage"]=out["answered"]/144
    out["useful_correct_resolution"]=out["correct"]/144
    out["answerable_correct_rate"]=out["correct"]/out["answerable"] if out["answerable"] else 0.0
    out["wrong_abstention_rate"]=out["wrong_abstention"]/out["answerable"] if out["answerable"] else 0.0
    out["provider_publication_rate"]=out["publications"]/out["provider_calls"] if out["provider_calls"] else 0.0
    return out


def summarize_families(rows):
    result={}
    by=defaultdict(list)
    for row in rows:
        by[row["family"]].append(row)
    require(set(by)==set(c209.c208.c207.FAMILIES),"Family coverage drift")
    for family in c209.c208.c207.FAMILIES:
        items=by[family]
        require(len(items)==16,"Family episode count drift:"+family)
        result[family]=dict(
            episodes=16,
            correct=sum(r["correct"] for r in items),
            answered=sum(bool(r["answer_emitted"]) for r in items),
            wrong_abstention=sum(r["wrong_abstention"] for r in items),
            attempts=sum(r["acquisition_attempts"] for r in items),
            provider_calls=sum(r["provider_calls"] for r in items),
            publications=sum(r["publications"] for r in items),
            user_turns=sum(r["user_turns"] for r in items),
            unnecessary_acquisition=sum(r["unnecessary_acquisition"] for r in items),
            missed_necessary_acquisition=sum(r["missed_necessary_acquisition"] for r in items),
        )
    return result


def measurement_complete(policy_summary,model_summary,rows):
    row_counts=Counter(r.get("policy_id") for r in rows)
    model_by={m.get("policy_id"):m for m in model_summary}
    candidate_ids=set(POLICY_IDS[2:])
    return (
        set(policy_summary)==set(POLICY_IDS)
        and set(row_counts)==set(POLICY_IDS)
        and all(row_counts[p]==144 for p in POLICY_IDS)
        and len(model_summary)==9
        and set(model_by)==candidate_ids
        and len(rows)==1584
        and all(policy_summary[p]["episodes"]==144 for p in POLICY_IDS)
        and policy_summary[POLICY_INTERNAL]["correct"]==48
        and policy_summary[POLICY_INTERNAL]["answered"]==48
        and policy_summary[POLICY_INTERNAL]["unresolved"]==96
        and policy_summary[POLICY_INTERNAL]["acquisition_attempts"]==0
        and policy_summary[POLICY_INTERNAL]["provider_calls"]==0
        and policy_summary[POLICY_INTERNAL]["publications"]==0
        and policy_summary[POLICY_INTERNAL]["user_turns"]==0
        and policy_summary[POLICY_INTERNAL]["authority_violation"]==0
        and policy_summary[POLICY_FIXED]["correct"]==128
        and policy_summary[POLICY_FIXED]["answered"]==128
        and policy_summary[POLICY_FIXED]["unresolved"]==16
        and policy_summary[POLICY_FIXED]["acquisition_attempts"]==96
        and policy_summary[POLICY_FIXED]["provider_calls"]==90
        and policy_summary[POLICY_FIXED]["publications"]==80
        and policy_summary[POLICY_FIXED]["user_turns"]==16
        and policy_summary[POLICY_FIXED]["authority_violation"]==0
        and policy_summary[POLICY_FIXED]["malformed_publication"]==0
        and all(policy_summary[p]["guarded_unsupported_assertion"]==0 for p in POLICY_IDS)
        and all(policy_summary[p]["authority_violation"]==0 for p in POLICY_IDS)
        and all(policy_summary[p]["malformed_publication"]==0 for p in POLICY_IDS)
        and all(m["initial_rows"]==144 for m in model_summary)
        and all(m["inference_rows"]==144+m["post_rows"] for m in model_summary)
        and all(
            policy_summary[pid]["inference_rows"]==model_by[pid]["inference_rows"]
            and policy_summary[pid]["inference_forward_calls"]==model_by[pid]["inference_forward_calls"]
            and policy_summary[pid]["inference_cell_calls"]==model_by[pid]["inference_cell_calls"]
            for pid in candidate_ids
        )
    )


def precheck(
    c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,
    c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
    c181_summary,c188_summary,root
):
    root=Path(root)
    p208,visible_path,pins,protected=c209.precheck(
        c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
        c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c209_summary)==PARENT_C209_SHA,"C209 summary changed")
    p209=audit.read_json(c209_summary)
    c209.validate_result(p209)
    require(
        p209.get("commit_sha")==PARENT_C209_EXECUTION
        and p209.get("status")=="PASS"
        and c209.gate(p209["summary"])
        and p209.get("source_blobs")==pins
        and p209.get("visible_sha256")==VISIBLE_SHA,
        "Wrong accepted C209 parent",
    )
    protected[str(Path(c209_summary).resolve())]=PARENT_C209_SHA
    for artifact in p209["artifacts"]:
        path=audit.safe_child(Path(c209_summary).resolve().parent,artifact["file"])
        require(
            path.is_file() and path.stat().st_size==artifact["serialized_bytes"]
            and audit.sha(path)==artifact["sha256"],
            "Changed C209 artifact:"+artifact["file"],
        )
        protected[str(path.resolve())]=artifact["sha256"]

    p207=audit.read_json(c207_summary)
    require(
        p207.get("scorer_sha256")==SCORER_SHA
        and p207.get("visible_sha256")==VISIBLE_SHA,
        "C207 development artifact identity drift",
    )
    scorer_path=None
    for artifact in p207["artifacts"]:
        if artifact["file"]=="development-scorer.json":
            scorer_path=audit.safe_child(Path(c207_summary).resolve().parent,artifact["file"])
            require(
                audit.sha(scorer_path)==SCORER_SHA
                and scorer_path.stat().st_size==artifact["serialized_bytes"],
                "C207 scorer artifact changed",
            )
            protected[str(scorer_path.resolve())]=SCORER_SHA
    require(scorer_path is not None,"C207 scorer artifact missing")

    pins=dict(pins)
    for rel,wanted in DIRECT_SOURCE_PINS.items():
        current=audit.git(root,"rev-parse","HEAD:"+rel).decode().strip()
        require(current==wanted,"Direct deciding-path source changed:"+rel)
        pins[rel]=wanted

    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins)==87 and len(protected)==165,"C210 source/protection count drift")
    require(digest(manifest())==MANIFEST_SHA,"C210 manifest drift")
    return p209,visible_path,scorer_path,pins,protected


def regression_modules(root):
    names=c209.regression_modules(root)
    require(len(names)==len(set(names))==94,"Historical regression module drift")
    return names+["tests_lm.test_v05_c210_baseline_development_measurement"]


def regression_suite(root):
    names=regression_modules(root)
    loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
    tests=list(c205._iter_tests(loaded))
    ids=[test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded)==1,"Historical dynamic test identity drift:"+excluded)
    kept=[test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests)==1998 and len(kept)==1997
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C210 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"]==EXPERIMENT_ID
        and payload["stage"]==STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C210",
    )
    require(
        len(payload["source_blobs"])==87
        and len(payload["input_sha256"])==165
        and len(payload["artifacts"])==5
        and {a["file"] for a in payload["artifacts"]}==OUTPUTS,
        "C210 coverage drift",
    )
    require(
        payload["numerical_margin_registration"] is False
        and payload["candidate_selection"] is False
        and payload["independent_holdout_created"] is False
        and payload["training_steps"]==0
        and payload["fresh_seed_count"]==0
        and payload["network_calls"]==0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C210 scope drift",
    )
    require(
        payload["status"]==(
            "PASS" if measurement_complete(
                payload["policy_summary"],payload["candidate_model_summary"],payload["episode_results"]
            ) else "FAIL"
        ),
        "C210 measurement-completeness gate drift",
    )


def run(
    *,c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,
    c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
    c181_summary,c188_summary,output_dir,expected_head
):
    root=Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()
                =="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    _,visible_path,scorer_path,pins,protected=precheck(
        c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,
        c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
        c181_summary,c188_summary,root
    )
    visible=audit.read_json(visible_path)
    scorer=audit.read_json(scorer_path)
    require(len(visible)==len(scorer)==144,"Frozen development alignment required")
    scorer_by={row["case_id"]:row for row in scorer}
    require(len(scorer_by)==144 and all(v["case_id"] in scorer_by for v in visible),
            "Scorer identity coverage drift")
    scorer_order=[scorer_by[v["case_id"]] for v in visible]

    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    bases,selectors=c204.restore_models(Path(c181_summary),Path(c188_summary))

    episode_rows=[]
    policy_summary={}
    family_summary={}
    candidate_model_summary=[]

    def new_envs():
        return [build_environment(v,s) for v,s in zip(visible,scorer_order,strict=True)]

    internal=attach_scores(
        [internal_only_policy(env) for env in new_envs()],visible,scorer_order
    )
    fixed=attach_scores(
        [fixed_acquisition_policy(env) for env in new_envs()],visible,scorer_order
    )
    episode_rows.extend(internal); episode_rows.extend(fixed)
    policy_summary[POLICY_INTERNAL]=summarize_policy(internal)
    policy_summary[POLICY_FIXED]=summarize_policy(fixed)
    family_summary[POLICY_INTERNAL]=summarize_families(internal)
    family_summary[POLICY_FIXED]=summarize_families(fixed)

    for b,h in CANDIDATE_PAIRS:
        envs=new_envs()
        raw_records,model_meter=candidate_pair_policy(envs,bases[b],selectors[b,h],b,h)
        scored=attach_scores(raw_records,visible,scorer_order)
        pid=f"CANDIDATE-{b}-{h}"
        episode_rows.extend(scored)
        policy_summary[pid]=summarize_policy(scored)
        policy_summary[pid]["inference_forward_calls"]=model_meter["inference_forward_calls"]
        policy_summary[pid]["inference_cell_calls"]=model_meter["inference_cell_calls"]
        family_summary[pid]=summarize_families(scored)
        candidate_model_summary.append(model_meter)
        print(
            f"[C210] {pid} correct={policy_summary[pid]['correct']} "
            f"answered={policy_summary[pid]['answered']} attempts={policy_summary[pid]['acquisition_attempts']} "
            f"provider_calls={policy_summary[pid]['provider_calls']}",
            flush=True,
        )

    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts=[]

    def record(name):
        path=out/name
        artifacts.append(dict(file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size))

    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)

    save("measurement-plan.json",dict(manifest(),source_blobs=pins))
    save("episode-results.json",episode_rows)
    save("policy-summary.json",policy_summary)
    save("family-summary.json",family_summary)
    save("candidate-model-summary.json",candidate_model_summary)

    guard()
    precheck(
        c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,
        c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
        c181_summary,c188_summary,root
    )
    for path,wanted in protected.items():
        require(audit.sha(path)==wanted,"Protected input changed:"+path)
    for artifact in artifacts:
        require(audit.sha(out/artifact["file"])==artifact["sha256"],"Output changed:"+artifact["file"])

    complete=measurement_complete(policy_summary,candidate_model_summary,episode_rows)
    result=dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        commit_sha=expected_head,
        status="PASS" if complete else "FAIL",
        diagnostic_execution_valid=True,
        C209_summary_sha256=PARENT_C209_SHA,
        visible_sha256=VISIBLE_SHA,
        scorer_sha256=SCORER_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        episode_results=episode_rows,
        policy_summary=policy_summary,
        family_summary=family_summary,
        candidate_model_summary=candidate_model_summary,
        policy_episode_evaluations=len(episode_rows),
        numerical_margin_registration=False,
        candidate_selection=False,
        independent_holdout_created=False,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        limitations=[
            "development measurement only; no performance acceptance margin",
            "all nine candidate model pairs retained; no winner selected",
            "shared symbolic/production-derived answer boundary is disclosed and not learned FOLD reasoning",
            "guarded unsupported assertions can be measured post-guard, but no learned answer-bit generator is present",
            "no independent holdout created or evaluated",
        ],
    )
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print("[C210] baseline development measurement collected",flush=True)
    print("=== C210 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c209-summary","c208-summary","c207-summary","c206-summary","c205-summary",
        "c204-summary","c203-summary","c202-summary","c201-summary","c200-summary",
        "c199-summary","c174-summary","c181-summary","c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
