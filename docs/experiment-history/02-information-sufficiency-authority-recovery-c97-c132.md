# Information sufficiency, authority and recovery — C97-C132

## Scientific subject

This sequence moved from "can a learned router tell when information is missing?" to "can an
external runtime safely own acquisition, evidence mutation, receipts, retries and recovery?"

The core architectural split established here is:

```text
model/controller -> proposes
runtime          -> authorizes, executes and mutates authoritative state
model/controller -> reobserves the resulting state
```

## Sufficiency and acquisition semantics — C97-C101

### C97 — oracle information sufficiency
PASS. The oracle acquired only when a missing hidden condition could change the answer.
Required acquisition recall=1.0, unnecessary acquisition rate=0, direct-answerable accuracy=1.0.

### C98 — learned sufficiency routing
PASS on an unseen visible base. The fixed-width Control Lane learned ANSWER/ACQUIRE from visible
inputs without receiving hidden truth or the oracle action.

### C99 — learned acquire/reobserve/answer cycle
PASS. Required rows acquired exactly once, answerable rows acquired zero times, every acquired row
answered after runtime evidence update, with zero repeat acquisitions or budget violations.

### C100 — acquisition-failure authority baseline
PASS. SUCCESS admitted evidence and continued to answer; UNAVAILABLE/DENIED/INVALID admitted no
evidence and terminated unresolved. Failed acquisition was explicitly defined as **not evidence**.

C101 and immediate follow-ups moved this outcome behavior from an oracle baseline toward learned
policy/runtime composition while preserving the same authority separation.

## Containment, idempotency and receipt authority — C102-C124

The subsequent experiments progressively hardened the closed loop against:

- unsafe fallback after failed acquisition;
- unseen-mask and feature-reencoding edge cases;
- stale eligibility and terminal refresh;
- post-preflight failure;
- unknown-effect containment;
- idempotency and receipt reconciliation;
- request/mechanism/epoch binding;
- provider/verifier authority;
- verdict scope and commit context;
- receipt replay.

A verified milestone is C120:
- 1,922 scenarios/seed;
- 480 exact-binding controls;
- 1,440 invalid-binding cases;
- valid binding accepted and invalid binding rejected/contained at rate1.0;
- no commit/retry/fallback on invalid binding.

The C121-C124 chain then strengthened "matching receipt" into "authoritative receipt in the correct
scope/context and replay state."

## Atomicity, restart and fencing — C125-C132

This range shifted from semantic routing to transactional/runtime safety:

- C125 atomic claim behavior;
- C126 restart recovery;
- C127 post-transition crash falsification;
- C128 concurrent recovery ownership;
- C129 recovery fencing;
- C130 lease renewal;
- C131 SQLite fencing;
- C132 OS-process fencing.

These experiments establish why later retrieval/evidence work can treat runtime ownership,
idempotency and recovery boundaries as explicit prerequisites rather than letting a model invent
state transitions.

## Durable conclusions

- "Need information" and "permission to obtain information" are separate variables.
- Evidence enters authoritative state only through validated runtime-owned transitions.
- Receipt/request/provider/scope identity is part of correctness, not metadata decoration.
- Retry/restart/concurrency must be bounded by ownership/fencing semantics.
- A high-quality model output cannot override runtime authority.

## Non-claims

This series did not yet establish real semantic retrieval relevance, natural-language reasoning,
or final Gate E behavior. Much of it used synthetic controlled tasks to define runtime contracts.

## Cleanup implication

The individual fault-injection scripts are strong archive candidates once dependency analysis shows
they are no longer imported by current regressions. The runtime primitives and tests encoding
authority, receipt binding, idempotency, fencing and recovery should not be removed merely because
the corresponding C-number is old.
