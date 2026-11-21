# C222 acceptance and C223 boundary

## Formal verdict

**C222 ACCEPTED PASS. Gate F remains NOT PASSED.**

Scientific execution HEAD: `ae4286ac9b79cd34eb8bdfd1d72ae2e27c308889`.
Published log commit: `ad285c5a318d7ac7b0067e07ffe06fb02edfb8e8`.
Log SHA256: `a0c24da2aebbab381a9325457bc12f7c6fd2046c36f9fdc32a5fd6fc7391fb5c`.
Summary SHA256: `18321ace4ade112fe227d4836867223a5ec609761c89015b704e9e14b629c62e`.
Local accepted summary:
`runs/c222-v5f-withdrawal-lifecycle-60ba479f7d2b46ff957b5d2a21bf865c/summary.json`.

## Execution validity

The receipt execution HEAD matches the registered C222 HEAD. The publication commit has that HEAD
as its parent. The published console reports 2401 focused tests in49.957 seconds, OK; source/
artifact prechecks and artifact postchecks passed; protected inputs preserved; clean tracked tree;
`diagnostic_execution_valid = true`, `lifecycle_gate = True`, `run_execution_valid = True`.

The review uses the published console/metadata and the runner's local artifact checks. It does not
claim reviewer-side access to or re-execution of the user's local-only checkpoint/artifact bytes.

## Deciding metrics

| Metric | Result |
|---|---:|
| Main successes | 1296/1296 |
| Forced-allow controls | 162/162 |
| Unrelated observed alpha anchor successes | 648/648 |
| Correct normal suppressions | 405/405 |
| Published beta answers after withdrawal | 0 |
| Downstream calls on normally suppressed queries | 0 |
| Exact lifecycle/provenance/export audits | 3/3 |
| Model fingerprints unchanged | true |
| New training steps | 0 |
| Model forwards | 3405 |

Main calls: Coverage1296; Selector/provider/bank/Reader891 each.
Forced-allow controls: Coverage/Selector/provider162 each; bank/Reader0.
Writer target accuracy1.0.

Artifact SHA256 values:
- lifecycle-plan.json: `1b94c0af7c1d828f54c5519dd9169a9e2a7985ddd91b155a72d312d39e26a828`
- timeline-audit.json: `ac64f295987df1d81ce774b53dc5e2f567e9119a05676a78834ec0b17e44c1cb`
- live-decisions.json: `ba5f2ca66e6c345e1da7cf4d6bea38c13addb2c9191d4b642702c504f610847d`
- forced-allow-decisions.json: `46d404627059f5e28653b498150ecda803e0ff057f02319cea10c730fb48ef09`
- validation-summary.json: `9d6916dfcaec497680b94ae2b280dc9ab98f3da17aac7447a8b2e8b150d9b40b`

## Interpretation

In the registered continuing synthetic state trajectory, the frozen learned stack stopped answering
from a withdrawn observed factor, did not revive it from a same-named hypothesis in another scope,
and kept an unrelated observed anchor readable. Symbolic RETRACTED remained distinct from MISSING;
Coverage intentionally suppressed both absent-observed cases, and END_SCOPE produced OUT_OF_SCOPE.
Hypotheses did not enter observed export or change the post-withdrawal H2 numeric state.

This is one trajectory per Writer, evaluated across81 checkpoint combinations. The1296 rows are
not1296 independent unseen tasks. Operation kinds and hypothesis construction remain oracle.

Important boundary: C222 rebuilds requests from each current state. An older QueryRequest still
closes over its original immutable state in the accepted C221 request factory. C222 therefore does
not establish freshness of retained requests or caches. No retroactive change to C222's gate is made.

## Next single question

C223 should test whether a session-owned request lease rejects retained requests after a state
publication, before any learned model/provider call, while fresh requests preserve C222 results.
The same lifecycle, checkpoints and operations remain fixed. Include representation-only commit
(memory revision unchanged) and explicit unguarded old-request replay controls. Do not add answer
caching, training, acquisition, new semantic tasks or memory-cost optimization in this experiment.

This document accepts C222 only. C223 remains NOT REGISTERED until its own registration and review.
