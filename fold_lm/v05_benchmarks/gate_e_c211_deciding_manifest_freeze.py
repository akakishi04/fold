"""C211: freeze the complete deciding Gate-E manifest without evaluating the holdout.

Use only accepted C210 development evidence to:
- select one candidate identity by deterministic tie-break among exact development ties;
- register numerical margins/statistical rules;
- construct and hash an independent nine-family holdout whose expression signatures are disjoint
  from C207 development;
- freeze budgets, baselines, output boundary, faults, stopping and invalidity.

No candidate/baseline inference is run on holdout cases in C211.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import unittest

from fold_lm.v05 import structured_derived_result as derived
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_e_c210_baseline_development_measurement as c210

EXPERIMENT_ID = "C211-v5e-deciding-manifest-freeze"
STAGE = "V5-E-DECIDING-MANIFEST-FREEZE"
BASE = "f17908d36d9f8d9ee2aa39f173e028a3b5bd6340"
PARENT_C210_EXECUTION = "002543b8d1394c127b915b3bfe4591ce20c8939d"
PARENT_C210_SHA = "1b4242f15fdf3ca48374660d5c3339ff5c17dc9cd4f4833852f5e1bccb349366"
DEVELOPMENT_VISIBLE_SHA = "c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543"
DEVELOPMENT_SCORER_SHA = "0591682848a69ac020a0f4a7bb2939e6df79ffd116567fe3c994a5f8e3fa3912"
SELECTED_POLICY = "CANDIDATE-181001-188001"
SELECTED_BASE_SEED = 181001
SELECTED_HEAD_SEED = 188001
BASE_CHECKPOINT_SHA = "3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289"
SELECTOR_CHECKPOINT_SHA = "02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d"
PROJECTION_BLOB = "346f7edab02ef1bc24db2934a1f0c6488ab5567c"
C210_POLICY_BLOB = "309e1a54a00ef828cea29f705e69d9a56df899d9"
MANIFEST_SHA = "8a24beda4da38c331b6c10ed4c46159073a78e1c426ccb580d9a861742e1db99"
FAMILIES = c210.c209.c208.c207.FAMILIES
UNITS_PER_FAMILY = 8
CONDITIONS = (0,1)
PAIR_VISIBLE_EQUAL = c210.c209.c208.c207.PAIR_VISIBLE_EQUAL
FAULTS = ("NONE","MALFORMED_PAYLOAD","MISSING_DELIVERY","PERMISSION_DENIED","BUDGET_EXHAUSTED")
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c211_deciding_manifest_freeze.py",
    "tests_lm/test_v05_c211_deciding_manifest_freeze.py",
    "tools/run_c211.ps1",
    "tools/invoke_c211.ps1",
    "docs/experiment-ledger-addendum-c211-preregistration.md",
    "docs/gate-e-deciding-manifest-v0.1.md",
)
OUTPUTS = {
    "deciding-manifest.json",
    "holdout-visible.json",
    "holdout-scorer.json",
    "holdout-units.json",
    "decision-rules.json",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def decision_rules():
    return dict(
        candidate=dict(
            policy_id=SELECTED_POLICY,
            base_seed=SELECTED_BASE_SEED,
            head_seed=SELECTED_HEAD_SEED,
            base_checkpoint_sha256=BASE_CHECKPOINT_SHA,
            selector_checkpoint_sha256=SELECTOR_CHECKPOINT_SHA,
            projection_blob=PROJECTION_BLOB,
            candidate_policy_blob=C210_POLICY_BLOB,
            selection_rule=(
                "all9 C210 candidate policy_summary and family_summary objects must be exactly "
                "equal; choose lexicographically smallest tied policy_id"
            ),
        ),
        baselines=[c210.POLICY_INTERNAL,c210.POLICY_FIXED],
        hard_zero_candidate=[
            "wrong_answer",
            "guarded_unsupported_assertion",
            "authority_violation",
            "malformed_publication",
            "invalid_target",
        ],
        fixed_noninferiority=dict(
            margin_episodes=0,
            overall=[
                ["correct",">="],
                ["answered",">="],
                ["wrong_abstention","<="],
                ["unnecessary_acquisition","<="],
                ["acquisition_attempts","<="],
                ["provider_calls","<="],
                ["user_turns","<="],
            ],
            per_family=[
                ["correct",">="],
                ["answered",">="],
                ["wrong_abstention","<="],
                ["unnecessary_acquisition","<="],
                ["user_turns","<="],
            ],
        ),
        internal_improvement=dict(
            minimum_margin_episodes=1,
            claims=[
                "useful_correct_resolution",
                "positive_acquisition_gain",
            ],
            test="one-sided exact paired McNemar",
            familywise_alpha=0.05,
            multiplicity="Holm over exactly2 primary improvement claims",
            holm_thresholds=[0.025,0.05],
        ),
        coverage=dict(
            noninferiority_margin_episodes=0,
            candidate_answered_must_be_at_least_fixed=True,
            wrong_abstention_must_be_no_more_than_fixed=True,
        ),
        unsupported_assertion_floor=dict(
            candidate_post_guard_required=0,
            internal_post_guard_development=0,
            strict_reduction_claim="NOT_DEMONSTRATED_ZERO_FLOOR",
        ),
        hard_runtime=dict(
            authority_violations=0,
            acquisition_budget_violations=0,
            malformed_evidence_publications=0,
            hypothesis_to_observation_promotions=0,
        ),
        candidate_compute_ceiling=dict(
            initial_inference_rows=144,
            maximum_post_inference_rows=144,
            maximum_total_inference_rows=288,
            maximum_forward_calls=2,
            maximum_cell_calls=14,
        ),
        output=dict(
            derived_schema=derived.SCHEMA,
            shared_answer_boundary=(
                "C171 completion_values + benchmark proof_fixture + production "
                "structured_derived_result.verify; disclosed symbolic guard"
            ),
            learned_unguarded_answer_generator_present=False,
        ),
        final_verdict=dict(
            pass_requires_all_rules=True,
            valid_rule_failure="ACCEPTED VALID NEGATIVE / Gate E NOT PASSED",
            no_family_removal=True,
            no_threshold_relaxation=True,
        ),
    )


def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        acceptance_base=BASE,
        parent_c210_execution=PARENT_C210_EXECUTION,
        parent_c210_sha256=PARENT_C210_SHA,
        development_visible_sha256=DEVELOPMENT_VISIBLE_SHA,
        development_scorer_sha256=DEVELOPMENT_SCORER_SHA,
        holdout_split="independent_deciding_holdout",
        families=list(FAMILIES),
        units_per_family=8,
        conditions_per_unit=2,
        dependence_units=72,
        episodes=144,
        episodes_per_family=16,
        semantic_independence=(
            "every holdout expression signature is disjoint from the C207 development expression "
            "signature set; units/case IDs are also disjoint; variable renaming alone is not used"
        ),
        candidate_policy=SELECTED_POLICY,
        candidate_selection="lexicographic exact-tie break after C210 development only",
        baseline_policies=[c210.POLICY_INTERNAL,c210.POLICY_FIXED],
        numerical_rules=decision_rules(),
        budgets=dict(
            maximum_acquisition_attempts_per_episode=1,
            maximum_dispatches_per_episode=1,
            maximum_proof_steps=derived.MAX_PROOF_STEPS,
            retry_failed_acquisition=False,
        ),
        registered_faults=list(FAULTS),
        source_schedule="one bounded source-bearing fact B in source-bearing families; same fault counts as development",
        output_schema=derived.SCHEMA,
        holdout_evaluated=False,
        model_forward_calls=0,
        baseline_policy_calls=0,
        scorer_used_for_policy=False,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="deciding registration freeze only; no holdout policy execution or Gate verdict",
    )


def _resources(channel=None, *, permitted=True, acquisitions=1):
    available=[False,False,False]
    permissions=[False,False,False]
    if channel is not None:
        idx=v2.CHANNELS.index(channel)
        available[idx]=True
        permissions[idx]=bool(permitted)
    return v1.Resources(
        internal_remaining=13,
        acquisitions_remaining=acquisitions,
        available=tuple(available),
        permitted=tuple(permissions),
        last_outcome="NONE",
        internal_step=7,
    )


def _channels(count, fact_index=None, channel=None):
    rows=[]
    for i in range(count):
        flags=[False,False,False]
        if i==fact_index and channel is not None:
            flags[v2.CHANNELS.index(channel)]=True
        rows.append(v2.FactChannels(tuple(flags)))
    return tuple(rows)


def _fact(fid,status="UNOBSERVED",value=None,refs=()):
    return v1.Fact(fid,status,value,tuple(refs))


def _base_view(case_id,nodes,facts,resources):
    unit_id=case_id.rsplit("-c",1)[0]
    scope="C211|"+unit_id
    return v1.TaskView(
        scope+"|query",scope,tuple(nodes),tuple(facts),resources,
        evidence_time=2,revision=1,
    )


def _eval(nodes,bits):
    stack=[]
    for node in nodes:
        if node.kind=="FACT":
            stack.append(int(bits[node.fact]) ^ int(node.negate))
        elif node.kind=="AND":
            stack.append(stack[node.left] & stack[node.right])
        else:
            stack.append(stack[node.left] | stack[node.right])
    return int(stack[-1])


def _binary_nodes(kind):
    require(kind in ("AND","OR"),"binary operator required")
    return (
        v1.Node("FACT",0,negate=1),
        v1.Node("FACT",1),
        v1.Node(kind,left=0,right=1),
    )


def _hard_nodes(unit):
    if unit % 2 == 0:
        # ((NOT A OR B) AND C) OR NOT D
        return (
            v1.Node("FACT",0,negate=1),
            v1.Node("FACT",1),
            v1.Node("OR",left=0,right=1),
            v1.Node("FACT",2),
            v1.Node("AND",left=2,right=3),
            v1.Node("FACT",3,negate=1),
            v1.Node("OR",left=4,right=5),
        )
    # NOT A AND (B OR (NOT C AND D))
    return (
        v1.Node("FACT",0,negate=1),
        v1.Node("FACT",1),
        v1.Node("FACT",2,negate=1),
        v1.Node("FACT",3),
        v1.Node("AND",left=2,right=3),
        v1.Node("OR",left=1,right=4),
        v1.Node("AND",left=0,right=5),
    )


def _binary_case(family,unit,condition,*,relevance,status,channel):
    kind="AND" if unit % 2 == 0 else "OR"
    control=(
        0 if kind=="AND" and relevance=="critical" else
        1 if kind=="OR" and relevance=="critical" else
        1 if kind=="AND" else
        0
    )
    case_id=f"H-{family}-u{unit:02d}-c{condition}"
    unit_id=f"H-{family}-u{unit:02d}"
    refs=()
    if status=="STALE":
        refs=(f"holdout-stale:{unit_id}:B",)
    elif status=="CONFLICT":
        refs=(f"holdout-conflict:{unit_id}:B:0",f"holdout-conflict:{unit_id}:B:1")
    facts=(
        _fact("A","OBSERVED",control,(f"holdout:{unit_id}:A",)),
        _fact("B",status,None,refs),
    )
    view=_base_view(case_id,_binary_nodes(kind),facts,_resources(channel))
    typed=v2.TaskView(view,_channels(2,1,channel))
    source_value=int(condition)
    conclusion=_eval(view.nodes,(control,source_value))
    return typed,dict(
        source_value=source_value,
        semantic_conclusion=conclusion,
        answerable_with_budget=True,
        necessary_fact_indices=[1] if relevance=="critical" else [],
        unnecessary_fact_indices=[] if relevance=="critical" else [1],
        expected_proposal=channel if relevance=="critical" else "ANSWER",
        expected_terminal="ANSWER",
        fault="NONE",
    )


def make_holdout_case(family,unit,condition):
    require(family in FAMILIES,"unknown family")
    require(type(unit) is int and 0 <= unit < 8,"unit out of range")
    require(condition in CONDITIONS,"condition out of range")
    case_id=f"H-{family}-u{unit:02d}-c{condition}"
    unit_id=f"H-{family}-u{unit:02d}"

    if family=="sufficient_known":
        bit=int(condition)
        nodes=(v1.Node("FACT",0,negate=1),)
        view=_base_view(
            case_id,nodes,
            (_fact("A","OBSERVED",bit,(f"holdout:{unit_id}:A",)),),
            _resources(),
        )
        typed=v2.TaskView(view,_channels(1))
        oracle=dict(
            source_value=None,semantic_conclusion=1-bit,answerable_with_budget=True,
            necessary_fact_indices=[],unnecessary_fact_indices=[],
            expected_proposal="ANSWER",expected_terminal="ANSWER",fault="NONE",
        )

    elif family=="answer_critical_hidden":
        typed,oracle=_binary_case(
            family,unit,condition,relevance="critical",status="UNOBSERVED",channel="RETRIEVE"
        )

    elif family=="conclusion_irrelevant_missing":
        typed,oracle=_binary_case(
            family,unit,condition,relevance="irrelevant",status="UNOBSERVED",channel="RETRIEVE"
        )

    elif family=="conflicting_evidence":
        typed,oracle=_binary_case(
            family,unit,condition,relevance="critical",status="CONFLICT",channel="OBSERVE"
        )

    elif family=="stale_evidence":
        typed,oracle=_binary_case(
            family,unit,condition,relevance="critical",status="STALE",channel="OBSERVE"
        )

    elif family=="noisy_malformed_evidence":
        kind="AND" if unit % 2 == 0 else "OR"
        control=0 if kind=="AND" else 1
        source_value=(unit+1)%2
        facts=(
            _fact("A","OBSERVED",control,(f"holdout:{unit_id}:A",)),
            _fact("B"),
        )
        view=_base_view(case_id,_binary_nodes(kind),facts,_resources("RETRIEVE"))
        typed=v2.TaskView(view,_channels(2,1,"RETRIEVE"))
        fault="NONE" if condition==0 else "MALFORMED_PAYLOAD"
        oracle=dict(
            source_value=source_value,
            semantic_conclusion=_eval(view.nodes,(control,source_value)) if fault=="NONE" else None,
            answerable_with_budget=(fault=="NONE"),
            necessary_fact_indices=[1],unnecessary_fact_indices=[],
            expected_proposal="RETRIEVE",
            expected_terminal="ANSWER" if fault=="NONE" else "UNRESOLVED",
            fault=fault,
        )

    elif family=="unavailable_acquisition":
        kind="AND" if unit % 2 == 0 else "OR"
        control=0 if kind=="AND" else 1
        source_value=(unit+1)%2
        fault="NONE"; permitted=True; acquisitions=1
        if condition==1:
            fault=("PERMISSION_DENIED","BUDGET_EXHAUSTED","MISSING_DELIVERY")[unit%3]
            permitted=fault!="PERMISSION_DENIED"
            acquisitions=0 if fault=="BUDGET_EXHAUSTED" else 1
        facts=(
            _fact("A","OBSERVED",control,(f"holdout:{unit_id}:A",)),
            _fact("B"),
        )
        view=_base_view(
            case_id,_binary_nodes(kind),facts,
            _resources("RETRIEVE",permitted=permitted,acquisitions=acquisitions),
        )
        typed=v2.TaskView(view,_channels(2,1,"RETRIEVE"))
        oracle=dict(
            source_value=source_value,
            semantic_conclusion=_eval(view.nodes,(control,source_value)) if fault=="NONE" else None,
            answerable_with_budget=(fault=="NONE"),
            necessary_fact_indices=[1],unnecessary_fact_indices=[],
            expected_proposal="RETRIEVE",
            expected_terminal="ANSWER" if fault=="NONE" else "UNRESOLVED",
            fault=fault,
        )

    elif family=="sufficient_reasoning_hard":
        nodes=_hard_nodes(unit)
        bits=(
            int(unit&1),
            int(condition),
            int((unit>>1)&1),
            int((unit+condition+1)&1),
        )
        facts=tuple(
            _fact(chr(65+i),"OBSERVED",bit,(f"holdout:{unit_id}:{chr(65+i)}",))
            for i,bit in enumerate(bits)
        )
        view=_base_view(case_id,nodes,facts,_resources())
        typed=v2.TaskView(view,_channels(4))
        oracle=dict(
            source_value=None,semantic_conclusion=_eval(nodes,bits),answerable_with_budget=True,
            necessary_fact_indices=[],unnecessary_fact_indices=[],
            expected_proposal="ANSWER",expected_terminal="ANSWER",fault="NONE",
        )

    elif family=="user_only_information":
        typed,oracle=_binary_case(
            family,unit,condition,relevance="critical",status="UNOBSERVED",channel="ASK_USER"
        )
    else:
        raise AssertionError("unreachable")

    packet=v2.encode(typed)
    require(v2.decode(packet)==typed,"holdout structured-v2 roundtrip drift")
    visible=dict(
        case_id=case_id,unit_id=unit_id,family=family,condition=condition,packet=asdict(packet)
    )
    scorer=dict(case_id=case_id,unit_id=unit_id,family=family,condition=condition,**oracle)
    return visible,scorer


def expression_signature_from_view(view):
    return tuple(
        (n.kind,n.fact,n.left,n.right,int(n.negate))
        for n in view.nodes
    )


def _view_from_visible(row):
    p=row["packet"]
    packet=v2.PolicyInput(
        p["schema"],tuple(p["features"]),
        v1.Binding(
            p["binding"]["request_id"],p["binding"]["scope_id"],
            tuple(p["binding"]["fact_ids"]),
            tuple(tuple(x) for x in p["binding"]["reference_ids"]),
        ),
    )
    return v2.decode(packet)


def generate_holdout():
    visible=[]; scorer=[]; units=[]
    for family in FAMILIES:
        for unit in range(UNITS_PER_FAMILY):
            cases=[]
            for condition in CONDITIONS:
                v,s=make_holdout_case(family,unit,condition)
                visible.append(v);scorer.append(s);cases.append(v["case_id"])
            units.append(dict(
                unit_id=f"H-{family}-u{unit:02d}",
                family=family,
                cases=cases,
            ))
    return visible,scorer,units


def validate_holdout(visible,scorer,units,development_visible):
    require(len(visible)==len(scorer)==144 and len(units)==72,"holdout size drift")
    visible_by={r["case_id"]:r for r in visible}
    scorer_by={r["case_id"]:r for r in scorer}
    require(len(visible_by)==len(scorer_by)==144,"duplicate holdout case ID")

    family_counts={f:0 for f in FAMILIES}
    fault_counts={x:0 for x in FAULTS}
    action_counts={"ANSWER":0,"RETRIEVE":0,"OBSERVE":0,"ASK_USER":0}
    channel_counts={x:0 for x in v2.CHANNELS}
    answerable=0
    hidden_payload_errors=0
    pair_errors=0

    for row in visible:
        family_counts[row["family"]]+=1
        require(set(row)=={"case_id","unit_id","family","condition","packet"},
                "visible holdout leakage/schema drift")
        view=_view_from_visible(row)
        for i,fact in enumerate(view.base.facts):
            if fact.status!="OBSERVED" and fact.value is not None:
                hidden_payload_errors+=1
            for channel in v2.declared_channels(view,i):
                channel_counts[channel]+=1

    for row in scorer:
        require(set(row)=={
            "case_id","unit_id","family","condition","source_value","semantic_conclusion",
            "answerable_with_budget","necessary_fact_indices","unnecessary_fact_indices",
            "expected_proposal","expected_terminal","fault",
        },"holdout scorer schema drift")
        fault_counts[row["fault"]]+=1
        action_counts[row["expected_proposal"]]+=1
        answerable+=int(row["answerable_with_budget"])

    for unit in units:
        require(len(unit["cases"])==2,"paired holdout unit required")
        c0,c1=unit["cases"]
        v0,v1row=visible_by[c0],visible_by[c1]
        s0,s1=scorer_by[c0],scorer_by[c1]
        family=unit["family"]
        equal=v0["packet"]==v1row["packet"]
        if family in PAIR_VISIBLE_EQUAL and not equal:
            pair_errors+=1
        if family=="unavailable_acquisition":
            if equal != (s1["fault"]=="MISSING_DELIVERY"):
                pair_errors+=1
        if family in ("sufficient_known","sufficient_reasoning_hard") and equal:
            pair_errors+=1
        if family in (
            "answer_critical_hidden","conclusion_irrelevant_missing",
            "conflicting_evidence","stale_evidence","user_only_information",
        ) and (s0["source_value"],s1["source_value"])!=(0,1):
            pair_errors+=1
        if family=="answer_critical_hidden" and s0["semantic_conclusion"]==s1["semantic_conclusion"]:
            pair_errors+=1
        if family=="conclusion_irrelevant_missing" and s0["semantic_conclusion"]!=s1["semantic_conclusion"]:
            pair_errors+=1

    dev_signatures={
        expression_signature_from_view(_view_from_visible(row).base)
        for row in development_visible
    }
    holdout_signatures={
        expression_signature_from_view(_view_from_visible(row).base)
        for row in visible
    }
    overlap=sorted(dev_signatures & holdout_signatures,key=repr)

    dev_units={row["unit_id"] for row in development_visible}
    holdout_units={row["unit_id"] for row in visible}
    dev_cases={row["case_id"] for row in development_visible}
    holdout_cases={row["case_id"] for row in visible}

    equal_units=sum(
        visible_by[u["cases"][0]]["packet"]==visible_by[u["cases"][1]]["packet"]
        for u in units
    )
    summary=dict(
        episodes=144,
        dependence_units=72,
        family_counts=family_counts,
        fault_counts=fault_counts,
        action_counts=action_counts,
        channel_episode_counts=channel_counts,
        answerable_with_budget=answerable,
        hidden_payload_errors=hidden_payload_errors,
        pair_errors=pair_errors,
        equal_visible_units=equal_units,
        development_expression_signatures=len(dev_signatures),
        holdout_expression_signatures=len(holdout_signatures),
        expression_signature_overlap=len(overlap),
        development_unit_overlap=len(dev_units & holdout_units),
        development_case_overlap=len(dev_cases & holdout_cases),
        holdout_evaluated=False,
        policy_calls=0,
        model_forward_calls=0,
    )
    return summary


def one_sided_mcnemar(candidate,baseline):
    require(
        type(candidate) is list and type(baseline) is list
        and len(candidate)==len(baseline)>0
        and all(type(x) is int and x in (0,1) for x in candidate+baseline),
        "paired binary vectors required",
    )
    better=sum(c==1 and b==0 for c,b in zip(candidate,baseline,strict=True))
    worse=sum(c==0 and b==1 for c,b in zip(candidate,baseline,strict=True))
    n=better+worse
    if n==0:
        return dict(better=0,worse=0,discordant=0,p_one_sided=1.0)
    numerator=sum(math.comb(n,k) for k in range(better,n+1))
    p=numerator/(2**n)
    return dict(better=better,worse=worse,discordant=n,p_one_sided=float(p))


def holm_two(pvalues,alpha=0.05):
    require(
        type(pvalues) is dict and len(pvalues)==2
        and all(type(v) in (int,float) and 0 <= v <= 1 for v in pvalues.values())
        and type(alpha) is float and 0 < alpha < 1,
        "exact two-claim Holm input required",
    )
    ordered=sorted(pvalues.items(),key=lambda x:(x[1],x[0]))
    first_name,first_p=ordered[0]
    second_name,second_p=ordered[1]
    first_pass=first_p <= alpha/2
    second_pass=first_pass and second_p <= alpha
    return dict(
        familywise_alpha=alpha,
        ordered=[list(x) for x in ordered],
        thresholds=[alpha/2,alpha],
        decisions={first_name:first_pass,second_name:second_pass},
        all_pass=bool(first_pass and second_pass),
    )


def _input_hash_suffix(payload,suffix):
    normalized=suffix.replace("\\","/").lower()
    matches=[
        value for key,value in payload["input_sha256"].items()
        if str(key).replace("\\","/").lower().endswith(normalized)
    ]
    require(len(matches)==1,"checkpoint identity suffix drift:"+suffix)
    return matches[0]


def freeze_candidate(p210):
    candidate_ids=list(c210.POLICY_IDS[2:])
    require(len(candidate_ids)==9,"C210 candidate identity count drift")
    first_policy=p210["policy_summary"][candidate_ids[0]]
    first_family=p210["family_summary"][candidate_ids[0]]
    require(
        all(p210["policy_summary"][x]==first_policy for x in candidate_ids)
        and all(p210["family_summary"][x]==first_family for x in candidate_ids),
        "C210 candidate development tie is not exact",
    )
    selected=min(candidate_ids)
    require(selected==SELECTED_POLICY,"candidate tie-break drift")
    require(
        _input_hash_suffix(p210,"probe-181001-INTERNAL_SEMANTICS.pt")==BASE_CHECKPOINT_SHA
        and _input_hash_suffix(p210,"selector-181001-188001.pt")==SELECTOR_CHECKPOINT_SHA,
        "selected checkpoint hash drift",
    )
    require(
        p210["source_blobs"]["fold_lm/v05/candidate_input_projection.py"]==PROJECTION_BLOB
        and p210["source_blobs"]["fold_lm/v05_benchmarks/gate_e_c210_baseline_development_measurement.py"]
            == C210_POLICY_BLOB,
        "selected candidate source identity drift",
    )
    return decision_rules()["candidate"]


def gate(summary,candidate,rules):
    return (
        summary.get("episodes")==144
        and summary.get("dependence_units")==72
        and summary.get("family_counts")=={f:16 for f in FAMILIES}
        and summary.get("fault_counts")=={
            "NONE":128,"MALFORMED_PAYLOAD":8,"MISSING_DELIVERY":2,
            "PERMISSION_DENIED":3,"BUDGET_EXHAUSTED":3,
        }
        and summary.get("action_counts")=={
            "ANSWER":48,"RETRIEVE":48,"OBSERVE":32,"ASK_USER":16,
        }
        and summary.get("channel_episode_counts")=={
            "RETRIEVE":64,"OBSERVE":32,"ASK_USER":16,
        }
        and summary.get("answerable_with_budget")==128
        and summary.get("hidden_payload_errors")==0
        and summary.get("pair_errors")==0
        and summary.get("equal_visible_units")==50
        and summary.get("expression_signature_overlap")==0
        and summary.get("development_unit_overlap")==0
        and summary.get("development_case_overlap")==0
        and summary.get("holdout_evaluated") is False
        and summary.get("policy_calls")==0
        and summary.get("model_forward_calls")==0
        and candidate.get("policy_id")==SELECTED_POLICY
        and rules==decision_rules()
    )


def precheck(
    c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,
    c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,
    c174_summary,c181_summary,c188_summary,root
):
    root=Path(root)
    p209,development_visible_path,development_scorer_path,pins,protected=c210.precheck(
        c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,
        c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
        c181_summary,c188_summary,root
    )
    require(audit.sha(c210_summary)==PARENT_C210_SHA,"C210 summary changed")
    p210=audit.read_json(c210_summary)
    c210.validate_result(p210)
    require(
        p210.get("commit_sha")==PARENT_C210_EXECUTION
        and p210.get("status")=="PASS"
        and c210.measurement_complete(
            p210["policy_summary"],p210["candidate_model_summary"],p210["episode_results"]
        )
        and p210.get("source_blobs")==pins
        and p210.get("visible_sha256")==DEVELOPMENT_VISIBLE_SHA
        and p210.get("scorer_sha256")==DEVELOPMENT_SCORER_SHA
        and p210.get("numerical_margin_registration") is False
        and p210.get("candidate_selection") is False
        and p210.get("independent_holdout_created") is False,
        "Wrong accepted C210 parent",
    )
    freeze_candidate(p210)
    protected[str(Path(c210_summary).resolve())]=PARENT_C210_SHA
    for artifact in p210["artifacts"]:
        path=audit.safe_child(Path(c210_summary).resolve().parent,artifact["file"])
        require(
            path.is_file() and path.stat().st_size==artifact["serialized_bytes"]
            and audit.sha(path)==artifact["sha256"],
            "Changed C210 artifact:"+artifact["file"],
        )
        protected[str(path.resolve())]=artifact["sha256"]

    pins=dict(pins)
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins)==89 and len(protected)==173,"C211 source/protection count drift")
    require(digest(manifest())==MANIFEST_SHA,"C211 manifest drift")
    return p210,development_visible_path,pins,protected


def regression_modules(root):
    names=c210.regression_modules(root)
    require(len(names)==len(set(names))==95,"Historical regression module drift")
    return names+["tests_lm.test_v05_c211_deciding_manifest_freeze"]


def regression_suite(root):
    names=regression_modules(root)
    loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
    tests=list(c205._iter_tests(loaded))
    ids=[test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded)==1,"Historical dynamic test identity drift:"+excluded)
    kept=[test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests)==2026 and len(kept)==2025
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C211 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"]==EXPERIMENT_ID
        and payload["stage"]==STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C211",
    )
    require(
        len(payload["source_blobs"])==89
        and len(payload["input_sha256"])==173
        and len(payload["artifacts"])==5
        and {a["file"] for a in payload["artifacts"]}==OUTPUTS,
        "C211 coverage drift",
    )
    require(
        payload["holdout_evaluated"] is False
        and payload["model_forward_calls"]==0
        and payload["baseline_policy_calls"]==0
        and payload["scorer_used_for_policy"] is False
        and payload["training_steps"]==0
        and payload["fresh_seed_count"]==0
        and payload["network_calls"]==0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C211 scope drift",
    )
    require(
        payload["status"]==(
            "PASS" if gate(payload["validation_summary"],payload["candidate"],payload["decision_rules"])
            else "FAIL"
        ),
        "C211 gate drift",
    )


def run(
    *,c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,
    c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,
    c174_summary,c181_summary,c188_summary,output_dir,expected_head
):
    root=Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()
                =="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    p210,development_visible_path,pins,protected=precheck(
        c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,
        c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,
        c174_summary,c181_summary,c188_summary,root
    )
    development_visible=audit.read_json(development_visible_path)
    visible,scorer,units=generate_holdout()
    validation=validate_holdout(visible,scorer,units,development_visible)
    candidate=freeze_candidate(p210)
    rules=decision_rules()

    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts=[]

    def record(name):
        path=out/name
        artifacts.append(dict(file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size))

    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)

    deciding=dict(
        registration_schema="fold-gate-e-deciding-manifest-v1",
        experiment_id=EXPERIMENT_ID,
        candidate=candidate,
        baselines=[c210.POLICY_INTERNAL,c210.POLICY_FIXED],
        holdout=dict(
            split="independent_deciding_holdout",
            episodes=144,dependence_units=72,
            visible_file="holdout-visible.json",
            scorer_file="holdout-scorer.json",
            units_file="holdout-units.json",
        ),
        decision_rules=rules,
        budgets=manifest()["budgets"],
        faults=list(FAULTS),
        output_schema=derived.SCHEMA,
        shared_answer_boundary=rules["output"]["shared_answer_boundary"],
        stopping=dict(
            execute_deciding_holdout_once=True,
            do_not_retrain_after_holdout=True,
            do_not_change_candidate_after_holdout=True,
            do_not_relax_thresholds_after_holdout=True,
            do_not_remove_failed_family=True,
        ),
        invalidity=dict(
            source_or_hash_drift="INVALID / RETRY SAME DECIDING C",
            incomplete_policy_or_family="INVALID / RETRY SAME DECIDING C",
            dirty_tree_or_head_drift="INVALID / RETRY SAME DECIDING C",
            valid_rule_failure="VALID NEGATIVE / Gate E NOT PASSED",
        ),
    )

    save("holdout-visible.json",visible)
    save("holdout-scorer.json",scorer)
    save("holdout-units.json",units)
    save("decision-rules.json",rules)

    deciding["holdout"]["visible_sha256"]=audit.sha(out/"holdout-visible.json")
    deciding["holdout"]["scorer_sha256"]=audit.sha(out/"holdout-scorer.json")
    deciding["holdout"]["units_sha256"]=audit.sha(out/"holdout-units.json")
    deciding["development_evidence"]=dict(
        C210_summary_sha256=PARENT_C210_SHA,
        C210_policy_summary_sha256=hashlib.sha256(
            json.dumps(p210["policy_summary"],sort_keys=True,separators=(",",":")).encode()
        ).hexdigest(),
        exact_candidate_tie=True,
    )
    deciding["validation_summary"]=validation
    save("deciding-manifest.json",deciding)

    guard()
    precheck(
        c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,
        c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,
        c174_summary,c181_summary,c188_summary,root
    )
    for path,wanted in protected.items():
        require(audit.sha(path)==wanted,"Protected input changed:"+path)
    for artifact in artifacts:
        require(audit.sha(out/artifact["file"])==artifact["sha256"],"Output changed:"+artifact["file"])

    result=dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        commit_sha=expected_head,
        status="PASS" if gate(validation,candidate,rules) else "FAIL",
        diagnostic_execution_valid=True,
        C210_summary_sha256=PARENT_C210_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        candidate=candidate,
        decision_rules=rules,
        validation_summary=validation,
        holdout_visible_sha256=deciding["holdout"]["visible_sha256"],
        holdout_scorer_sha256=deciding["holdout"]["scorer_sha256"],
        holdout_units_sha256=deciding["holdout"]["units_sha256"],
        deciding_manifest_sha256=audit.sha(out/"deciding-manifest.json"),
        holdout_evaluated=False,
        model_forward_calls=0,
        baseline_policy_calls=0,
        scorer_used_for_policy=False,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        limitations=[
            "registration freeze only; holdout policy execution is forbidden in C211",
            "selected candidate is a deterministic tie-break among exact C210 development ties",
            "guarded unsupported-assertion comparative reduction is not demonstrated because internal baseline is already at zero floor",
            "final Gate E verdict requires a later one-shot deciding holdout execution under this exact manifest",
        ],
    )
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print("[C211] deciding Gate E manifest frozen",flush=True)
    print("=== C211 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c210-summary","c209-summary","c208-summary","c207-summary","c206-summary",
        "c205-summary","c204-summary","c203-summary","c202-summary","c201-summary",
        "c200-summary","c199-summary","c174-summary","c181-summary","c188-summary",
        "output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
