# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C238 ACCEPTED PASS (minimal seen-TRAIN fitting). C239 NOT REGISTERED. C240 NOT REGISTERED.**
No active experiment during acceptance-to-registration transition.
C236 remains ACCEPTED VALID NEGATIVE; C237 remains diagnostic-integrity PASS only.

## Latest accepted evidence — C238

Scientific execution HEAD: `a7999c92e2f6f071c045de268feaf5ddd6f438ac`.
Published log commit: `93a86ea4493c4c6bf20b046b56c29e8bccc322f9`.
Log SHA256: `da9386a9f351ebf9aeec18df7057aac9971c4b068fbe337efdcf7363260b8e60`.
Summary SHA256: `06ab54549477894ea17f986364cacc6b3b7d25ff2dea70b18e98e2a957c80363`.
Local summary: `runs/c238-v5b-complete-cohort-sampler-df6538e306784434bdcbb2848e4c278d/summary.json`.

24 own tests PASS in3.553s;2881 focused tests PASS in72.485s.274 source pins/406 protected inputs.
Six models x400 updates:2400 steps/76800 answer presentations;2454 total forwards/77664 rows.
Initial/final replays, changed weights and recorded C236 comparator checks PASS.
Protected inputs preserved;tracked tree clean;execution HEAD preserved;run_execution_valid=True.

All12 cells:100% accuracy (8/8),fact/query pairs4/4,evidence/query mask drops50 percentage points.
C236 had50% accuracy,0/4 pairs and0 mask drops. Both Full and GRU-only now pass every criterion.
The registered sampler intervention was sufficient for this observed improvement, but does not
isolate coverage versus balance versus gradient variability. Memorization remains possible.
No general-language, unseen-generalization, core-superiority or Gate F claim.

Acceptance/artifact identities: docs/experiment-ledger-addendum-c238-c239.md.
Acceptance record commit: `72907fe195f56b886a9bc9b9fc0db6c83f9cbda2`.
Acceptance is based on published evidence/postcheck, not a reviewer checkpoint rerun or full-log rehash.

## Preserved earlier evidence

C237 diagnostic PASS: internal numerical responses without correct answer switching.
Details: docs/experiment-ledger-addendum-c237-c238.md.
C236 valid negative on16 prompts with random replacement batches; do not rewrite or rerun it.
Details: docs/experiment-ledger-addendum-c236-c237.md.
C235 diagnostic PASS: failure already on complete TRAIN, not only EVAL; first invalid attempt preserved.
C234/C233 remain valid negatives; C232 remains bounded template-byte learning only.

## Next boundary

Prepare C239 order-transfer: fresh models, order0 TRAIN8 and order1 HOLDOUT8 from the same fixed16 pool.
Keep complete-cohort batch32, optimizer and400 steps. Never initialize from C238 trained states.
The exact prompts/row IDs are disjoint; underlying assignments/questions are intentionally shared.
Only separate preregistration and independent post-authoring review may activate C239.

## Stop and scope

Gate F NOT PASSED; numeric-memory tuning paused. Preserve accepted sources/tests/logs and
 tools/run_c167.ps1. No history rewrite, cleanup, paid API, external corpus, larger model or
production runtime change. Judge each C before registering its successor.
