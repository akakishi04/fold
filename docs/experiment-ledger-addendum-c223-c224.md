# C223 acceptance and C224 cost-measurement boundary

## Formal verdict

**C223 ACCEPTED PASS. C224 NOT REGISTERED by this document. Gate F NOT PASSED.**

Scientific execution HEAD: `cdcc1d4211a149003f44dbdbd18a7e5367c013ab`.
Published log commit: `6e96f798b4c931247f58ab9982b617780d0ee9db`.
Log SHA256: `aff5dbc06d2c85ae54b2181dd2605c09dab66388f758626ce8e3e056bdbe0601`.
Summary SHA256: `1b08cf76a1c233ce849f2b7fe81dbb7fa44120e59a75b32e2f42c4ebccdad2ca`.
Local summary:
`runs/c223-v5f-request-freshness-56cfd6d212764ccf98e7789aa964de52/summary.json`.
Validation SHA256: `b52c9d95bb89dca5061d2ccff4aab90276ea5dc4edba2d653b1d9fdc03d12db2`.

## Execution validity and deciding evidence

Published metadata identifies the registered execution HEAD. The log reports2435 focused tests
in67.788 seconds, OK, scientific_status PASS, freshness_gate True, preserved protected inputs,
clean tracked tree and run_execution_valid True. Scientific execution and log publication commits
are distinct. This review uses published console evidence and the recorded local artifact checks;
it does not claim reviewer-side re-execution of the user's local checkpoints.

| Metric | Result |
|---|---:|
| Fresh successful decisions / exact C222 parity | 1296 /1296 |
| Old-generation leases rejected | 4536 /4536 |
| Stale-result exposures | 0 |
| Coverage /Selector /provider /bank /Reader calls on stale leases | 0 /0 /0 /0 /0 |
| Same-generation repeat successes | 81 /81 |
| Intentionally unguarded replay controls reproducing old behavior | 324 /324 |
| Writer target accuracy | 1.0 |
| New training | 0 |
| Total model forwards | 4134 |

## Accepted claim and limits

For explicitly published trusted immutable states within one process, the session generation guard
rejects retained old requests before any learned model or provider call while preserving current
answers. Representation-only H1/H2 commit also invalidates old leases. A still-current lease remains
reusable. Bypassing the new guard intentionally reproduces stale behavior in the registered controls.

This is one synthetic lifecycle crossed with81 checkpoint combinations, not thousands of independent
unseen problems. It does not establish answer-cache invalidation, concurrent/distributed execution,
in-place tensor mutation detection, malicious-bypass protection, learned operation-kind selection,
natural-language quality, acquisition or bounded total memory cost. Gate F is not passed.

## Next single question

The recent integration/lifecycle correctness checks are now established in their narrow scope.
The next experiment should measure, rather than assume, the outstanding Gate F storage/read-cost
claim: how does the existing H1/H2 reference compare with full raw-history replay as the number of
revisions grows, when raw evidence, source lookup index and provenance are counted?

C224 is proposed as a **measurement/attribution pilot**, not a new compression optimization and not
a Gate F decision. Use the same retained evidence in both arms, separate persisted bytes from warm
query work, and do not call a smaller capsule payload a smaller complete memory system.
A faithful audit may PASS even when the measured candidate costs more storage; any superiority
claim must be reported separately from measurement validity.
