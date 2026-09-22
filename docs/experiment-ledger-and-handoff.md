# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C221 ACCEPTED PASS. C222 ACTIVE / NOT YET JUDGED. C223 NOT REGISTERED.**

C222 is the unique ACTIVE experiment. Do not execute before post-authoring review PASS.

## Accepted C221

Scientific execution HEAD: `ed82010bede050c0209be8b540d83cc544fa6bd4`.
Published log commit: `438de3443827bada6d4dcdb02b37404aca4194a0`.
Log SHA256: `17e43c428a0d90708bb6e242fa2308e97c95d74f87e5188820a7f4b5a1dfb39a`.
Summary SHA256: `70cee94a95b20d538d86a041a3518151f019e03d15594132720c041224859766`.
Local summary:
`runs/c221-v5f-live-coverage-dispatch-cbcaaf2ea8b94d7a8b748426810f442b/summary.json`.

Focused regression2369/2369 OK. Main648/648, exact C220 parity648/648,
readable486/486, distinct suppression162/162, causal controls324/324.
Suppressed main queries made zero downstream calls. Fingerprints unchanged; training0;
model forwards2109; protected inputs preserved; run_execution_valid True.

Main calls: Coverage648 /Selector486 /provider486 /bank486 /Reader486.
Controls: Coverage324 /Selector162 /provider162 /bank0 /Reader0.
Full verdict: `docs/experiment-ledger-addendum-c221-c222.md`.

Evidence is published console/metadata plus recorded local artifact checks, not reviewer-side
re-execution of the user's local checkpoint bytes. C221 establishes actual Coverage-first
invocation, while C220 remains accepted as offline composition. Neither is broad generalization.

## Accepted V5-F chain and limits

C213 MemoryOp/provenance; C214 numeric closure; C215 H1/H2 commit;
C216 Reader; C217 Selector; C218 factor+relation Writer; C219 Coverage;
C220 offline composition; C221 causal live dispatch.

All neural components remain small structured-input pilots. Not established: natural language,
learned operation kinds, broad unseen tasks, arbitrary stale request/cache handling, acquisition,
bounded indexing or total memory-cost superiority. Gate F is not passed.

## Active C222 — withdrawal and hypothesis lifecycle

Experiment: `C222-v5f-withdrawal-hypothesis-lifecycle`.
Stage: `V5-F-WITHDRAWAL-HYPOTHESIS-LIFECYCLE`.

One question: after withdrawing a committed observation, does the frozen live stack stop publishing
it even with a same-named hypothesis in another scope, while retaining an unrelated observed anchor?

Change only the evaluation lifecycle. No new/changed production module; all neural checkpoints and
C221 dispatch/provider logic frozen. Operation kinds and ASSUME construction remain oracle.

One continuing state chain per Writer:
anchor_only -> beta_hot -> beta_committed -> beta_replaced -> beta_retracted -> shadow_assumed ->
shadow_ended -> project_ended.

Alpha is an observed class1 anchor throughout. Beta initially class2, then class0 after REPLACE,
then no answer after RETRACT. ASSUME sandbox/beta class2 must not revive project/beta.
Symbolic project/beta remains RETRACTED until project END_SCOPE, then OUT_OF_SCOPE.
Hypotheses never export as observed evidence. H2 W/b remain unchanged after withdrawal.

Each snapshot queries alpha and beta via a fresh current-state request. Old request closure/cache
reuse is not exercised. Eight snapshots x2 queries x81 combinations =1296 main decisions:
891 readable /405 suppressed. These are not1296 independent unseen tasks.

Force Coverage allow at the retracted and hypothesis-live snapshots:162 controls must stop at the
provider with BLOCKED_MISSING, no bank/Reader call. Alpha must remain correct648/648.
Require1296 main successes,162 control successes, zero beta answers after RETRACT, zero normal
suppression downstream calls and three exact lifecycle/provenance/export audits.

Successful calls:
main Coverage1296 /Selector891 /provider891 /bank891 /Reader891;
controls Coverage162 /Selector162 /provider162 /bank0 /Reader0.
Writer forwards3; total model forwards3405; training0.

Source pins171; protected inputs207; direct dependencies17; OWN6; outputs5.
New tests32; modules107; loaded2402 /focused2401, inherited exact exclusion1.
Manifest SHA: `1b94c0af7c1d828f54c5519dd9169a9e2a7985ddd91b155a72d312d39e26a828`.
Registration: `docs/experiment-ledger-addendum-c222-preregistration.md`.
Design: `docs/v5f-withdrawal-hypothesis-lifecycle-v0.1.md`.

## C222 post-authoring review

**post_authoring_review = PENDING**

Author-side30 targeted synthetic/spy tests passed with the exact accepted dispatcher source.
Parent-tree-dependent tests2, actual accepted numerical trajectory, full2401 regression, Windows
AST parsing and local-only checkpoint execution remain unexecuted here. The authoritative runner
executes all32 new tests before full regression and science. Do not represent the synthetic tests
as a pass of pending parent-tree or checkpoint checks.

## Historical evidence and maintenance

Prior state remains at
`438de3443827bada6d4dcdb02b37404aca4194a0:docs/experiment-ledger-and-handoff.md`.
Gate E decisive log: `docs/experiment-run-logs/c212/latest.log`.
Preserve accepted sources and `tools/run_c167.ps1` historical regression infrastructure.
No cleanup, history rewrite, new CI or Actions-storage work. Actions storage is handled separately.

## Stop condition

Judge C222 before any C223 registration.
Complete gate miss: scientific FAIL. Source/artifact/schema/regression or incomplete trajectory:
INVALID / RETRY SAME C222. Gate F remains NOT PASSED.
