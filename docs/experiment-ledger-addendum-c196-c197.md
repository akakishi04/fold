# C196 acceptance / C197 handoff

## Formal judgment

**C196 — ACCEPTED PASS.**
**C197 NOT REGISTERED at this acceptance commit.**
Gate E remains **NOT PASSED**.

Successful C196:
- scientific execution HEAD: `c1a4e68c785fab6441dd08892588add81f9486d6`
- published log commit: `5a2605a9bac234a605b9f35394520fff2175db82`
- log SHA256: `b7b8f4d6c80cd31f855611584d7b6260c839510a2ecad6167c2f9925ea773a84`
- log bytes: 358094
- summary: `runs/c196-v5e-result-aware-loop-ebea1cb9c1e248fb837f92ae653ecfed/summary.json`
- summary SHA256: `b0de25067be3fb9ab24486e2936a62b26f6cf0446f3b85f7e97f7cb932d7e6fb`
- focused regression: **1629/1629**, 49.408s
- source/artifact precheck PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

## Deciding evidence

Two full arms, each 9 selector blocks x9536 = **85824 episodes**.

### ALLOWED

The result-aware loop reproduced accepted C194 exactly:
- failed0 in all 9 blocks
- reference replay errors0
- reference block mismatches0
- necessity prediction errors0
- target prediction errors0
- max active necessity logit delta0.0
- max active target logit delta0.0
- first reads85824
- second reads34948
- third reads8352
- final authoritative decision rows8352
- total reads129124

### PERMISSION_REVOKED_AFTER_DECISION

The model makes the same initial learned decision on an allowed state. Then trusted scheduler
refresh revokes RETRIEVE permission before the action proposal.

Across all **85824** denied-arm episodes:
- one learned decision / episode
- exactly one DENIED/PERMISSION_DENIED attempt / episode
- denied attempts85824
- actual provider reads0
- provider calls0
- publications0
- receipts0
- retries0
- fake SUFFICIENT0
- fact mutation0
- resource/status errors0
- failed0

Per selector:9536 learned decisions and9536 denied attempts, with zero reads/retries.

The denied final resource contract is:
```text
internal_remaining 11
acquisitions_remaining 4
RETRIEVE permission false
last_outcome PERMISSION_DENIED
internal_step 9
```

## Scientific interpretation

C196 establishes that the generic learned acquisition loop must be **result-aware** rather than
"attempt-aware": it re-enters only after an acquisition is actually admitted/published.

A learned NEEDS/target decision made while authority was initially valid cannot force execution
after the trusted runtime revokes permission. The denied attempt creates no provider work, evidence,
receipt, retry or fabricated completion.

This extends the earlier C187 single-step authority result into the accepted generic loop.

## Non-claims

- only first-acquisition, post-decision permission revocation was tested;
- no in-flight provider failure yet;
- no stale-reservation / attempt-limit generic-loop test yet;
- no learned retry/resource/tool/provider policy;
- no independent holdout, language, answer/proof, or full Gate E completion.

## Next boundary

C197 should keep C196 result-aware loop, budget13, models, cohort and source worlds fixed and change
only the first acquisition endpoint outcome:

> after the learned decision and successful runtime reservation, the provider is actually invoked
> once and raises the registered ProviderFailure. Does the result-aware loop terminate unresolved
> after that failed dispatch, with no evidence/publication/receipt/retry/fake SUFFICIENT?

This is distinct from C196:
- C196 is denied **before provider execution**;
- C197 should fail **during provider execution after reservation**.
