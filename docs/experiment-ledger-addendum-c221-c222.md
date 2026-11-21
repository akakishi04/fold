# C221 acceptance and C222 boundary

## Formal verdict

**C221 ACCEPTED PASS. Gate F remains NOT PASSED.**

Scientific execution HEAD: `ed82010bede050c0209be8b540d83cc544fa6bd4`.
Published log commit: `438de3443827bada6d4dcdb02b37404aca4194a0`.
Log SHA256: `17e43c428a0d90708bb6e242fa2308e97c95d74f87e5188820a7f4b5a1dfb39a`.
Summary SHA256: `70cee94a95b20d538d86a041a3518151f019e03d15594132720c041224859766`.
Validation artifact SHA256: `c3ed8f149357c27281122b3cab9876b371d8da25a57dd536fa4e1b32f0a7ab0c`.

Accepted local summary:
`runs/c221-v5f-live-coverage-dispatch-cbcaaf2ea8b94d7a8b748426810f442b/summary.json`.

## Execution validity

The published metadata execution HEAD matches the registered C221 HEAD. The publication commit is
its direct child, with message `logs(fold): publish C221 execution log`.
The log reports the2369-test focused suite OK in59.425 seconds, scientific PASS,
`live_dispatch_gate = True`, preserved protected inputs, clean tracked tree and
`run_execution_valid = True`.

Acceptance is based on the published log and metadata. The local-only checkpoint/artifact bytes
have not been downloaded to the reviewer; their integrity is evidenced by the runner's recorded
source/artifact precheck and postcheck, not an independent reviewer-side re-execution.

## Deciding metrics

| Metric | Result |
|---|---:|
| Main decisions / successes | 648 /648 |
| Exact C220 answer and Coverage parity | 648 /648 |
| Readable successes | 486 /486 |
| Correct distinct suppressions | 162 /162 |
| Causal control decisions / successes | 324 /324 |
| Downstream calls on main suppression | 0 |
| All component fingerprints unchanged | true |
| Writer target accuracy | 1.0 |
| New training steps | 0 |
| Total model forwards | 2109 |

Main call totals: Coverage648, Selector486, provider486, bank reads486, Reader486.
Control call totals: Coverage324, Selector162, provider162, bank reads0, Reader0.
Writer forwards3. Traces follow the registered branch-specific call order.

Registered artifacts:
- dispatch-plan.json: `fb387b9c026ee852f4efbabab0c71cde93e03fea443f440f7b508b8fe3c3f4d8`
- live-decisions.json: `bf3ecc6de4accc2346e27a2a5d2a3955afdd762e01d14fc4ebce8f1877e93454`
- intervention-decisions.json: `38256d249c523d2534f152b68d1568161fd84d26d271a5316de0c92e3158eb0a`
- component-fingerprints.json: `2b600e9a46171c03914687d3288308e517db3fb95844327eba0a803a50a961a7`
- validation-summary.json: `c3ed8f149357c27281122b3cab9876b371d8da25a57dd536fa4e1b32f0a7ab0c`

## Interpretation and limits

Unlike C220's offline composition, C221 verifies actual Coverage-first downstream invocation.
Forced suppression stops downstream calls. Forced false-allow proposals on MISSING/OOS reach the
provider, whose independent deterministic preconditions stop numeric reads and Reader calls.
Those preconditions are runtime safety checks, not learned guarantees.

These are eight reused synthetic episode shapes crossed with81 checkpoint combinations, plus
four intervention types crossed with81 combinations. They are not648 independent new problems.
No natural-language ability, acquisition integration, trained operation selection, cache freshness
across arbitrary retained requests, total memory-cost advantage or Gate F completion is established.

## Next single question

C222 should evaluate withdrawal and hypothesis non-resurrection on one continuing state trajectory:
can the same frozen live stack stop publishing a committed observation after RETRACT, even when a
same-named hypothesis exists in another scope, while preserving an unrelated observed factor?

Add only this lifecycle evaluation (ASSERT/COMMIT/REPLACE/RETRACT/ASSUME/END_SCOPE), retaining the
accepted production memory and dispatch modules unchanged. Rebuild each query request from the
current immutable state; do not claim a solution for reuse of an old request closure or an answer
cache. Keep operation kind oracle and all neural checkpoints frozen.

C222 is NOT REGISTERED by this acceptance document. Its own registration and review determine
execution permission. Actions-storage work stays separate.
