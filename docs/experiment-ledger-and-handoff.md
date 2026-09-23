# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C237 ACCEPTED PASS (diagnostic integrity only). C238 NOT REGISTERED. C239 NOT REGISTERED.**
No active experiment during acceptance-to-registration transition.
C236 and C234 remain ACCEPTED VALID NEGATIVE. C235 remains diagnostic-integrity PASS only.

## Latest accepted evidence — C237

Scientific execution HEAD: `2dec1314181d62fbdf0a7d4c52007a9360921fd2`.
Published log commit: `f59b0012e488978f5733c4e8669eabc74ae47ad6`.
Log SHA256: `f4f6328ca74d96f21ee498da3d1d06f2e754d2abb70a51f0a15a0eccc22361db`.
Summary SHA256: `056fcbe4ebd2f888c0d5d5aa2761a18cd4229ed4af428e8e298d7af3abf55b32`.
Local summary: `runs/c237-v5b-frozen-signal-audit-8dbdc04fdad84f49b41a78388ad0b7fb/summary.json`.

24 own tests PASS;2857 focused tests PASS.36 model forwards/576 row presentations;zero training.
144 paired plus192 masked contrasts;12 cells. Parent/passive replays and unchanged fingerprints PASS.
Persisted trace/contrast replay PASS.268 source pins/394 inputs protected;run_execution_valid=True.

All48 query-change and48 assignment-swap pairs have different encoder EOS vectors, but all keep
the same answer and0/48 pairs are both correct. Every printed cell has nonzero maximum downstream
readout/logit response. Numerical sensitivity is not learned binding or a causal diagnosis.

Acceptance/artifact details: `docs/experiment-ledger-addendum-c237-c238.md`.
Acceptance commit: `4794376d53aba9e01c780b8569f1db75f64ca952`.
No C236 verdict change, generalization or Gate F promotion.

## Preserved C236 comparator

C236 ACCEPTED VALID NEGATIVE. All12 cells:50% accuracy,0/4 fact/query pairs,zero mask drops.
Execution HEAD: `0bc91722ca27803f065d2458505b502a2d01e50f`.
Summary SHA256: `0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec`.
Local summary: `runs/c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71/summary.json`.
Details: docs/experiment-ledger-addendum-c236-c237.md.
Do not rerun or modify C236. Its initial/final measurements remain separate identities.

## Earlier evidence and next boundary

C235: diagnostic integrity PASS; failure already on complete TRAIN. Details in
experiment-ledger-addendum-c235-c236.md; its initial invalid attempt is retained in its recovery log.
C234/C233 remain valid negatives; C232 remains bounded template-byte learning only.

Prepare C238 as a one-variable sampler intervention relative to C236: same16 rows, fresh initial
weights, batch32 and400 steps, but every row appears exactly twice in every batch instead of
replacement sampling. This is a hypothesis, not a cause inferred from C237. Separate registration
and authoring review are required before activation. No capability result is assumed.

## Stop and scope

Gate F NOT PASSED; numeric-memory tuning paused. Preserve accepted sources/tests/logs and
 tools/run_c167.ps1. No history rewrite, cleanup, paid API, external corpus or larger model.
Judge each active C before registering its successor.
