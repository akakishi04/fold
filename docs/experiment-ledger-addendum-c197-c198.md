# C197 acceptance / C198 handoff

## Formal judgment

**C197 — ACCEPTED PASS.**
**C198 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful C197:
- scientific execution HEAD: `7d9a09bba9ac2286806f40bc20c6ce45a21cb279`
- published log commit: `b6f2cb6334c22f435320e0f2204b894152bd4797`
- log SHA256: `2053ea31d161e732fb496ea1213612bafc4869df75aef3bdaa3ecbcd460581c6`
- log bytes: 363536
- summary: `runs/c197-v5e-provider-failure-reason-952131896bd7469296cda4621436c043/summary.json`
- summary SHA256: `632e8af4a215d12adc83aa015da855c63605205c87832aa6a511dabfc4fd1ca5`
- focused regression: **1653/1653**
- source/artifact precheck PASS
- Python syntax preflight PASS
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- production runtime modified False; Gate E candidate False

The earlier C197 attempt at `675af144558c9528a8cde9e79d20a0c447736b72` remains
**INVALID EXECUTION / RETRY SAME C197** evidence only; it failed before scientific execution
because two generated Python call sites contained literal backslash-n text. The accepted run
uses the recovery HEAD above and does not revise the scientific manifest.

## Deciding evidence

Two complete arms, each 9 selector blocks x 9536 = **85824 episodes**.

### ALLOWED

The accepted C196/C194 path was replayed under the C197 wrapper.

- 9/9 blocks complete
- reference replay errors 0
- scientific errors 0
- registered read-depth behavior preserved
- active necessity/target logit deltas within the fixed tolerance

### PROVIDER_FAILURE_AFTER_RESERVATION

Across all **85824** episodes:

- failure attempts: 85824
- provider calls: 85824
- actual fault-adapter calls: 85824
- action: PENDING / ACQUISITION_RESERVED
- dispatch: UNRESOLVED / PROVIDER_FAILURE
- generic-loop terminal cause: PROVIDER_FAILURE
- publications: 0
- receipts: 0
- retries: 0
- fact mutation: 0
- fake SUFFICIENT: 0
- candidate gate passed: True

Registered final resource contract is preserved:
```text
internal_remaining      9
acquisitions_remaining  3
RETRIEVE available      1
RETRIEVE permitted      1
last_outcome            NONE
internal_step           11
pending                  none
runtime terminal         none
```

## Scientific interpretation

C197 establishes, in this bounded repeatedly inspected development family, that the generic
result-aware loop can preserve the actual **post-reservation provider failure cause** instead
of collapsing it to the earlier action-level `ACQUISITION_RESERVED` reason.

The failed provider call creates no admitted observation, evidence publication, receipt,
retry or fabricated semantic completion. The accepted C196 ALLOWED behavior remains intact.

This is evidence for orchestration failure-cause propagation, not learned provider reliability.

## Non-claims

C197 does not establish:
- generic retry policy;
- stale-reservation handling in the generic loop;
- attempt-limit handling in the generic loop;
- later-step authority changes;
- learned resource/tool/provider policy;
- independent final holdout;
- language, answer, proof, or full Gate E completion.

## Next boundary

The next smallest untested in-flight boundary is reservation invalidation.

C198 should hold the accepted C197/C196 loop, budget13, frozen models, cohort and source worlds
fixed. After the first learned NEEDS/target decision and a successful RETRIEVE reservation,
the trusted scheduler should refresh the TaskView so that the evidence identity changes
**before dispatch**.

Question:

> Does the generic loop terminate as `UNRESOLVED_ACQUISITION_STALE_RESERVATION`, with the
> dispatch returning `REJECTED / STALE_RESERVATION`, zero provider call, zero publication,
> zero receipt, zero retry and no fake SUFFICIENT?

This differs from:
- C196: authority revoked before reservation;
- C197: reservation remains current and the provider itself fails;
- C198: reservation becomes stale before the provider is called.
