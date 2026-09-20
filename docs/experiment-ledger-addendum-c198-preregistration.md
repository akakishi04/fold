# C198 preregistration — stale reservation after successful reservation

**C197 ACCEPTED PASS. C198 ACTIVE / NOT YET JUDGED. C199 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

With the accepted C197 reason-aware / C196 result-aware generic loop held fixed, if the
first RETRIEVE action is successfully reserved and the trusted scheduler then advances the
visible evidence identity before dispatch, does the old reservation fail as
`STALE_RESERVATION` without provider execution, evidence publication, receipt, retry,
fact mutation or fake SUFFICIENT?

This is the next in-flight boundary after:
- C196: permission revoked before reservation/provider execution;
- C197: reservation remains current, provider is invoked, provider fails;
- C198: reservation succeeds, then becomes stale before provider invocation.

## Single changed condition

Only the first acquisition path in the stale arm changes:

```text
learned NEEDS + target
-> ActionResult PENDING / ACQUISITION_RESERVED
-> trusted owner.refresh()
     evidence_time += 1
     revision      += 1
     facts/resources/authority unchanged
-> dispatch(old intent)
-> REJECTED / STALE_RESERVATION
-> terminal generic-loop cause STALE_RESERVATION
```

The evidence identity refresh is scheduler-owned. It is not a policy action and supplies no
new hidden fact value.

The ALLOWED arm performs no refresh and must reproduce the accepted C197 allowed arm.

## Held constant

- budget13;
- C174 PILOT NEEDS cohort;
- 9536 coherent-world episodes / selector;
- 9 frozen C181 x C188 selector pairs;
- 16 coherent C190/C191 source bindings;
- C172/C173 runtime semantics;
- C196 result-aware continuation;
- C197 dispatch-reason propagation;
- max_dispatches3;
- teachers and raw argmax;
- checkpoints / seeds / training;
- production runtime.

No source world, label, model, threshold, action authority or provider implementation is
changed by the scientific intervention.

## Parent / reference artifact contract

Accepted C197:
- scientific execution HEAD:
  `7d9a09bba9ac2286806f40bc20c6ce45a21cb279`
- summary:
  `runs/c197-v5e-provider-failure-reason-952131896bd7469296cda4621436c043/summary.json`
- summary SHA256:
  `632e8af4a215d12adc83aa015da855c63605205c87832aa6a511dabfc4fd1ca5`

C198 has its own C197 prediction loader. Required NPZ keys:

```text
necessity_predictions
necessity_logits
target_predictions
target_logits
row_indices
local_rows
world_codes
```

Required shapes:

```text
necessity_predictions (2,9,9536,4)
necessity_logits      (2,9,9536,4,2)
target_predictions    (2,9,9536,3)
target_logits         (2,9,9536,3,4)
row_indices           (9536,)
local_rows            (9536,)
world_codes           (9536,)
```

The C197 ALLOWED arm (index0) is the direct prediction/logit reference.

## Arms

### 1. ALLOWED

Full 9536 episodes x9 selectors.

Requirements:
- exact C197 allowed prediction replay;
- necessity/target prediction errors0;
- active finite logit deltas <=1e-6;
- exact first/second/third/final row counts;
- exact provider read count;
- all existing accepted scientific counters0.

### 2. STALE_RESERVATION_AFTER_RESERVATION

Full 9536 episodes x9 selectors.

For every episode:
- the initial learned NEEDS/target decision is exactly the accepted C197 initial output;
- one action is PENDING / ACQUISITION_RESERVED;
- acquisition reservation consumes one acquisition;
- trusted refresh advances evidence_time and revision exactly +1;
- facts, resources and authority are unchanged by refresh;
- dispatch returns REJECTED / STALE_RESERVATION;
- dispatch internal_charged=1;
- provider_calls=0;
- actual provider file reads=0;
- fact_publications=0;
- receipts=0;
- no second learned decision;
- retries=0;
- fact mutation=0;
- no fake SUFFICIENT.

Required final visible coordinates:

```text
internal_remaining      10
acquisitions_remaining  3
RETRIEVE available      1
RETRIEVE permitted      1
last_outcome            NONE
internal_step           10
evidence_time           initial + 1
revision                initial + 1
pending                 none
runtime terminal        none
```

Required orchestration status:

```text
UNRESOLVED_ACQUISITION_STALE_RESERVATION
```

## Fixed gate

ALLOWED, all9 blocks:
- episodes9536;
- exact C197 allowed replay;
- all historical scientific counters0;
- reference prediction errors0;
- active logit deltas<=1e-6;
- registered read-depth/read-count identity exact.

STALE_RESERVATION_AFTER_RESERVATION, all9 blocks:
- episodes9536;
- stale_attempts9536;
- provider_calls0;
- actual_provider_reads0;
- publications0;
- receipts0;
- learned_decisions9536;
- retries0;
- initial reference prediction errors0;
- initial logit deltas<=1e-6;
- all stale/status/resource/identity/fact/fake-sufficient error counters0.

All18 blocks must satisfy their arm gate.

A finite completed miss is **ACCEPTED VALID NEGATIVE**.
Source/hash/schema/parent artifact/loader/nonfinite/incomplete/protection/execution failure is
**INVALID EXECUTION / RETRY SAME C198**.

No result may change this preregistered gate, cohort, seeds, intervention or threshold.

## Interpretation boundary

PASS supports only this bounded statement:

> the accepted generic loop preserves a stale-reservation rejection occurring after a valid
> reservation and before provider invocation, without performing provider work or fabricating
> evidence/completion.

PASS does not establish:
- generic retry/recovery after staleness;
- ATTEMPT_LIMIT handling in the generic loop;
- arbitrary concurrent refresh;
- multi-process reservation fencing;
- learned resource/tool/provider policy;
- independent final holdout;
- language, answer, proof, or Gate E completion.

## Workload / authoring quality gate

- 2 arms x85824 episodes =171648 episodes;
- 9 blocks / arm;
- expected focused regression **1677 =1653 existing +24 new**;
- expected regression modules **83**;
- historical source pins **151**;
- protected paths **396**;
- output artifacts **5** excluding summary;
- no new training / fresh seeds / network / proof checking / answer generation;
- production runtime modified False;
- Gate E candidate False.

New tests include:
- manifest/self-hash;
- C197 NPZ schema and exact shapes;
- one-row real action-runtime/acquisition-owner integration;
- reservation occurs before refresh;
- refresh occurs before dispatch;
- provider callback is a fail-if-called sentinel;
- exact STALE_RESERVATION result/status;
- exact resource/evidence identity coordinates;
- no receipt/fact mutation/retry;
- gate-negative controls.

The runner performs Python py_compile before source/artifact precheck, then the full 1677
focused regression before the scientific benchmark.

Scientific manifest SHA256:
`e108bcaefdb882f05420c078a4866272afe375d48e62e50ac726241fed2a44e9`.

## Execution / stop condition

Use the final registration HEAD as `ExpectedHead`.

Expected progress:
- C198 repository preflight
- C198 authoring syntax preflight
- source_and_artifact_precheck = PASS
- focused regression 1677/1677
- 18 block progress lines
- RESULT
- POSTCHECK
- remote log publication

Stop and keep **C198** active if execution is INVALID.
Do not register C199 until C198 is formally judged.
