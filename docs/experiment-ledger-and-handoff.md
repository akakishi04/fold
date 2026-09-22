# FOLD Experiment Ledger and Handoff

Follow `AGENTS.md` and `docs/experiment-conversation-handoff-protocol.md` (response format v2).
Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C221 ACCEPTED PASS. C222 NOT REGISTERED.**

No ACTIVE experiment while the next child is authored.

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
re-execution of the user's local checkpoint bytes.

## Interpretation boundary

C221 establishes causal Coverage-first invocation on eight reused synthetic episode shapes,
not648 independent unseen tasks. False readable proposals are additionally blocked by deterministic
provider scope/presence preconditions; this is not learned safety.

C220 remains accepted as offline composition; C221 closes its actual-call-order limitation.
All neural components remain small structured-input pilots. Gate F is not passed.

## Accepted V5-F chain

C213 MemoryOp/provenance; C214 numeric closure; C215 H1/H2 commit;
C216 Reader; C217 Selector; C218 factor+relation Writer; C219 Coverage;
C220 offline composition; C221 actual Coverage-first dispatch.

Not established: natural language, learned operation kinds, broader unseen tasks, withdrawal and
hypothesis lifecycle in the live stack, acquisition integration, bounded indexes or total memory
cost superiority. Do not infer memory-cost savings from small numeric tensors alone.

## Next boundary

C222 proposed question: does a continuing frozen-stack state trajectory stop publishing a revoked
observation, including while a same-named hypothesis exists in another scope, without losing an
unrelated observed anchor?

Add only lifecycle evaluation. Production memory/dispatcher modules and checkpoints stay fixed.
Operation kind remains oracle. Each request is rebuilt from current state; old request/cache reuse
is explicitly outside the claim. No retraining, acquisition, indexing optimization or new CI.

## Historical evidence and maintenance

Prior detailed state remains at
`438de3443827bada6d4dcdb02b37404aca4194a0:docs/experiment-ledger-and-handoff.md`.
Gate E decisive log: `docs/experiment-run-logs/c212/latest.log`.
Preserve accepted sources and `tools/run_c167.ps1` historical regression infrastructure.
No script/log cleanup, history rewrite or Actions-storage change is part of the next experiment.
Actions storage is being handled separately by the user.

## Stop condition

C222 remains NOT REGISTERED until authoring and committed-source review are complete.
Gate F remains NOT PASSED.
