# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C235 ACCEPTED PASS (diagnostic integrity only). C236 NOT REGISTERED. C237 NOT REGISTERED.**
No active experiment during the acceptance-to-registration transition.
C234 remains ACCEPTED VALID NEGATIVE. C235 is not a binding capability PASS.

## Latest accepted evidence — C235

Scientific execution HEAD: `fc3311955c3dcda87b67c2ee8dd58a59fb256d6f`.
Published log commit: `71dd1bb48978a1bd0a6b71448f1ceb29011696c4`.
Log SHA256: `fb2811d896606c07bd3d6cbd28a036d30f905dfce0295ade1fde582cde14b40a`.
Summary SHA256: `a9d6daa76bab38488ec3634d186ba81a2d61ae878df80202f3084057e917b1b5`.
Local summary: `runs/c235-v5b-frozen-binding-diagnostic-17d75b38b35249a297bde78cee0f1d43/summary.json`.

24 own tests PASS;2809 focused tests PASS.36 forwards /10368 row presentations /zero new training.
All parent EVAL replays and frozen-weight fingerprints pass;256 source pins/370 inputs preserved.
Tracked tree clean, execution HEAD preserved, run_execution_valid=True.
All12 cells: TRAIN_ACCURACY_BELOW_90. TRAIN accuracy47.9167%-53.125%.
TRAIN supplied-value rate100%; query-change same-answer rate78.125%-94.7917%.
Failure is already on TRAIN, not only held-out EVAL. No internal causal mechanism is established.

Acceptance: `docs/experiment-ledger-addendum-c235-c236.md`.
Acceptance commit: `dc0b43a197bfa9061bd2454099e41111cc4dd17c`.
The first invalid attempt remains at log commit1615b5ce54afed8bde44ac9d326cace6c6e674d0 and in
`docs/experiment-ledger-addendum-c235-execution-recovery.md`; it is not erased by the valid retry.

## Preserved C234 evidence

C234 ACCEPTED VALID NEGATIVE; full_binding_gate=False and gru_binding_gate=False.
Scientific execution HEAD: `c225c2d82636085e2d639878738e1b9a7aa37b42`.
Published log commit: `930fa77881d60558b3199b980f139ddef8bcb6ee`.
Summary SHA256: `a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523`.
Local summary: `runs/c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200/summary.json`.
Full EVAL19/96-25/96 correct; GRU-only30/96-39/96. Binding not demonstrated under the fixed recipe.
Full details/artifact identities: `docs/experiment-ledger-addendum-c234-c235.md`.
C233 remains ACCEPTED VALID NEGATIVE; C232 remains bounded template-byte learning only.

## Next boundary

C236 is being prepared as a separate minimal16-row TRAIN binding probe; it is not registered here.
No increase in model size or training steps, no changed parent task renderer, no checkpoint
continuation or favorable seed selection, and no C234 threshold rescue.
Only a reviewed preregistered launcher may activate the next experiment.

## Numeric-memory track and stop

C230 prepared route remains optional; numeric-memory tuning stays paused. Gate F is not waived.
Preserve all accepted sources/tests/logs and tools/run_c167.ps1.
No cleanup/history rewrite, paid API, external corpus, larger model or production runtime change.
Judge each active C before registering its successor.
