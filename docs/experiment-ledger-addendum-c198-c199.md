# C198 acceptance / C199 handoff

## Formal judgment

**C198 — ACCEPTED PASS.**
**C199 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C198:
- scientific execution HEAD: `e5a09864497fa38a9eac8d400b5162e33e99ec0d`
- published log commit: `49fcb1145acdcf3efd20afb5edf2740585265655`
- log SHA256: `f8f0de3e15725926bba692dba294b402763c480ac7e63965cda795d6644a0dee`
- log bytes: 369756
- summary: `runs/c198-v5e-stale-reservation-c8dcde8fca5c4cc2979475d64b7c2fda/summary.json`
- summary SHA256: `9cbb99e6ad200c5a9b88438abf140c58dd293661d8765f3460e3d2a7c70a8e75`
- focused regression: **1677/1677** in 87.36s
- all 18 registered arm/block progress records completed with failed=0
- source/artifact precheck PASS
- Python syntax preflight PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

## Deciding evidence

Two complete arms, each 9 selector blocks x9536 = **85824 episodes**.

### ALLOWED

The accepted C197/C196/C194 path was replayed:
- 9/9 blocks complete
- reference prediction errors0
- registered read-depth behavior preserved
- scientific error counters0
- active finite logit deltas within the fixed tolerance

### STALE_RESERVATION_AFTER_RESERVATION

Across all **85824** episodes:
- stale reservation attempts85824
- action reservation succeeds before refresh
- trusted refresh advances evidence_time and revision exactly +1
- dispatch returns REJECTED / STALE_RESERVATION
- generic-loop terminal cause STALE_RESERVATION
- provider calls0
- actual provider reads0
- publications0
- receipts0
- retries0
- fact mutation0
- fake SUFFICIENT0
- identity_refresh_error0
- resource_error0
- status_error0
- candidate_gate_passed True

Registered final stale-arm resource contract is preserved:
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
runtime terminal         none
```

## Scientific interpretation

C198 establishes, in this bounded repeatedly inspected development family, that the accepted
generic loop rejects an acquisition reservation whose evidence identity became stale after
reservation and before provider invocation. The stale reservation does not reach the provider,
does not publish evidence and does not re-enter the learned loop.

Together with C196/C197 this now covers three distinct first-acquisition interruption points:
- authority denial before reservation/provider execution;
- stale reservation after reservation but before provider execution;
- provider failure after reservation and provider invocation.

## Non-claims

C198 does not establish:
- retry/recovery after staleness;
- generic-loop ATTEMPT_LIMIT handling;
- arbitrary concurrent refresh or multi-process fencing;
- learned resource/tool/provider policy;
- independent final holdout;
- language, answer, proof, or full Gate E completion.

## Next boundary

The remaining explicit bounded dispatch guard not yet exercised in the generic learned loop is
`ATTEMPT_LIMIT`.

C199 should hold the accepted models, budget13 cohort, source worlds and generic loop semantics
fixed, and change only the AcquisitionOwner dispatch limit from3 to1 in the intervention arm.

Question:

> after one successful admitted acquisition, when the learned policy requests a second
> acquisition, does the already accepted generic loop preserve `ATTEMPT_LIMIT`, avoid a
> second provider call/publication, stop without a third learned decision, and avoid fake
> SUFFICIENT?

Rows that become SUFFICIENT after the first observation must still terminate normally and must
not be forced into the limit path.
