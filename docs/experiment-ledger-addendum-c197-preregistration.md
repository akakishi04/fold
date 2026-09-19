# C197 preregistration — provider-failure reason propagation

**C196 ACCEPTED PASS. C197 ACTIVE / NOT YET JUDGED. C198 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can one orchestration change preserve the accepted C196 ALLOWED behavior and safely expose a
post-reservation provider failure as the generic-loop terminal unresolved cause?

The single changed rule is:

```text
if acquisition was not admitted:
    if a dispatch result exists:
        unresolved reason = dispatch.reason
    else:
        unresolved reason = action.reason
```

C196 already proved that continuation is result-aware. C197 does not change that continuation
criterion. It changes only failure-reason propagation at the generic-loop boundary.

## Why this boundary exists

Source inspection after C196 acceptance showed that the C196 loop used `action.reason` when an
acquisition was not admitted. That is correct for the permission-denied arm because no dispatch
exists, but it would hide an in-flight provider failure behind `ACQUISITION_RESERVED`.

C197 therefore distinguishes:

- pre-dispatch authority denial — already accepted in C196;
- post-reservation provider failure — new C197 condition.

## Arms

### 1. ALLOWED

Full accepted C196/C194 path:
- 9536 worlds / selector;
- 9 selectors;
- exact prediction/logit replay;
- identical first/second/third/final row counts;
- identical actual read counts.

### 2. PROVIDER_FAILURE_AFTER_RESERVATION

The same initial state, model decision, target, resources and SourceBinding are used.
Only Endpoint.fetch changes: it is invoked once and raises the registered
`structured_acquisition_lifecycle.ProviderFailure`.

Expected episode path:

```text
budget13 state
-> learned NEEDS + target
-> runtime ActionResult PENDING / ACQUISITION_RESERVED
-> acquisition budget reserved
-> exactly one provider call
-> DispatchResult UNRESOLVED / PROVIDER_FAILURE
-> no evidence publication
-> no receipt
-> no loop retry
-> terminal orchestration status UNRESOLVED_ACQUISITION_PROVIDER_FAILURE
```

Expected final resource coordinates:

```text
internal_remaining      9
acquisitions_remaining  3
RETRIEVE available      1
RETRIEVE permitted      1
last_outcome            NONE
internal_step            11
pending                  none
runtime terminal         none
```

`last_outcome=NONE` is the existing C173 structured-resource contract because
PROVIDER_FAILURE is not one of the model-visible `task.OUTCOMES`. C197 does not redesign it.

## Held constant

- budget13;
- C174 cohort;
- 9 frozen C181/C188 pairs;
- 16 coherent C190/C191 source bindings;
- C172/C173 runtime semantics;
- accepted C196 result-aware continuation rule;
- max_dispatches3;
- raw argmax;
- scoring teachers;
- no training/fresh seeds/checkpoint changes;
- no production runtime modification.

## Fixed gate

ALLOWED, every selector:
- episodes9536;
- all accepted C196/C194 scientific counters0;
- first reads9536;
- exact second/third/final/read block counts;
- reference prediction errors0;
- active logit deltas <=1e-6.

PROVIDER_FAILURE_AFTER_RESERVATION, every selector:
- episodes9536;
- failure attempts9536;
- provider calls9536;
- actual fault-adapter calls9536;
- initial C194 necessity/target replay exact, logit deltas <=1e-6;
- each action PENDING/ACQUISITION_RESERVED;
- each dispatch UNRESOLVED/PROVIDER_FAILURE;
- publications0;
- receipts0;
- learned decisions9536;
- retries0;
- fact mutation0;
- fake SUFFICIENT0;
- exact resources9/3/available1/permitted1/outcomeNONE/step11;
- orchestration status preserves PROVIDER_FAILURE;
- all failure/scoring counters0.

All9 selectors in both arms must pass.

A finite completed miss is **ACCEPTED VALID NEGATIVE**.
Hash/schema/precheck/nonfinite/incomplete/protection/execution failure is
**INVALID EXECUTION / RETRY SAME C197**.

## Interpretation boundary

PASS means the generic loop now preserves the actual post-reservation provider failure cause while
remaining result-aware and without retry/evidence fabrication.

PASS does not establish:
- generic retry policy;
- stale-reservation or attempt-limit handling in this loop;
- learned resource/tool/provider policy;
- independent final holdout;
- language/answer/proof;
- Gate E completion.

## Workload and authoring quality gate

- 2 arms x85824 episodes
- 9 blocks/arm
- source pins146
- protected paths385
- artifacts5 excluding summary
- expected focused regression **1653 =1629 existing +24 new**
- expected modules82
- new 1-row integration test exercises actual:
  reservation -> provider call -> ProviderFailure -> no retry -> resources9/3/step11
- C197 reuses C196 loop implementation; wrapper changes only terminal reason selection
- C194 loader remains the accepted C196 loader; no new prediction schema is introduced
- launcher publishes C197 log remotely

Scientific manifest SHA256:
`7f7121c336e68dc58578e35f75b7c459986f5adbd2329344fc08514e468d58d2`.
