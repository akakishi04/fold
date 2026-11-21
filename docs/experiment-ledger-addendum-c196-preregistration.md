# C196 preregistration — result-aware generic loop

**C195 ACCEPTED PASS. C196 ACTIVE / NOT YET JUDGED. C197 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can one result-aware continuation rule preserve accepted C194 behavior and safely stop after
a permission-denied acquisition when RETRIEVE authority is revoked after the learned decision
but before the first acquisition proposal?

## Changed variable

Only generic-loop continuation semantics change:

```text
old:
acquisition attempt
-> always re-enter loop

C196:
acquisition attempt
-> re-enter only if action reserved AND dispatch PUBLISHED/OBSERVATION_ADMITTED
-> otherwise terminate UNRESOLVED with the acquisition reason
```

No model, checkpoint, teacher, source, budget or action-runtime implementation changes.

## Fixed arms

### ALLOWED

Budget13, same accepted C194 workload:
- 9536 coherent-world episodes / selector
- 9 frozen selector pairs
- exact C194 necessity/target predictions
- active finite logit deltas <=1e-6
- exact first/second/third/final row counts and actual reads

This arm verifies the changed continuation rule is a no-op when acquisitions are admitted.

### PERMISSION_REVOKED_AFTER_DECISION

The learned iteration0 decision is produced on the original allowed TaskView.
After that decision and before acquisition proposal, the trusted scheduler performs one
`refresh()` changing only RETRIEVE permission true->false.

Expected per episode:
- one learned decision
- one learned target
- exactly one acquisition attempt
- ActionResult status DENIED
- reason PERMISSION_DENIED
- internal_charged1
- acquisition_reserved0
- dispatch None
- provider calls0
- publications0
- receipts0
- retries0
- no second learned inference
- no fact/evidence mutation
- status `UNRESOLVED_ACQUISITION_PERMISSION_DENIED`
- final resource coordinates: internal11, acquisitions4, RETRIEVE permission0,
  last_outcome PERMISSION_DENIED, step9
- runtime terminal remains None; no fake SUFFICIENT

The permission change occurs **after** the learned decision, so iteration0 learned outputs must
remain exact to accepted C194.

## Fixed gate

All 9 ALLOWED blocks:
- episodes9536
- scientific errors0
- C194 prediction errors0
- active logit deltas<=1e-6
- per-block read-depth/final-decision counts exact
- actual reads exact

All 9 denial blocks:
- episodes9536
- denied attempts9536
- learned decisions9536
- actual provider reads0
- provider calls0
- publications0
- receipts0
- retries0
- all denial/runtime/resource/fact/fake-sufficient errors0
- initial necessity/target predictions exact C194
- initial active logit deltas<=1e-6

A completed finite failure of the result-aware continuation rule is
**ACCEPTED VALID NEGATIVE**.
Source/hash/schema/parent-artifact identity/loader/nonfinite infrastructure/incomplete/
protection failure is **INVALID EXECUTION / RETRY SAME C196**.

## Interpretation boundary

PASS means the generic loop can:
1. preserve the previously accepted admitted-acquisition path exactly; and
2. stop after one dynamically permission-denied acquisition without retrying, fabricating
   evidence or claiming semantic completion.

PASS does not establish provider-failure, stale-reservation, attempt-limit, later-step
authority revocation, learned resource policy, tool/provider choice, independent holdout,
language, answer/proof, or Gate E completion.

## Workload

- ALLOWED:85824 episodes
- PERMISSION_REVOKED_AFTER_DECISION:85824 episodes
- 9 selector blocks /arm
- artifacts5 excluding summary
- source pins141
- protected paths374
- expected regression **1629 =1605 existing +24 new**
- expected modules81
- production runtime modifiedFalse
- Gate E candidateFalse

## Authoring quality gate

Before user execution:
- C194 prediction artifact uses a C196-owned schema loader;
- result-aware loop continues only under explicit `admitted(acq)`;
- permission refresh occurs after phase target recording and before `c190.acquire`;
- synthetic ALLOWED integration covers three admissions + final SUFFICIENT;
- synthetic denial integration covers one DENIED/PERMISSION_DENIED, zero provider reads,
  zero retry, final resources11/4/permission0/outcome2/step9;
-21 parent summaries registered;
-precheck receives C195 +20 prior summaries +root;
-postcheck ExpectedHead is argv23;
-new tests24,total1629,modules81;
-log publisher configured for C196.

Scientific manifest SHA256:
`cbbbcdac61d729e6c73a86d6e3c70ed74189db33bb4c9c2ea557becb630a2457`.
