# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C236 ACCEPTED VALID NEGATIVE. C237 NOT REGISTERED. C238 NOT REGISTERED.**
No active experiment during the acceptance-to-registration transition.
C235 remains diagnostic-integrity PASS only; C234 remains ACCEPTED VALID NEGATIVE.

## Latest accepted evidence — C236

Scientific execution HEAD: `0bc91722ca27803f065d2458505b502a2d01e50f`.
Published log commit: `46e453a7e3900085002479791c6544b8669b9cf0`.
Log SHA256: `784bba560a4b9a9d168def96314ef9da36df4d9594d913ed526b1e0f297a92e8`.
Summary SHA256: `0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec`.
Local summary: `runs/c236-v5b-minimal-binding-9cc3975f1c304ea893b8b53104ee8f71/summary.json`.

24 own tests PASS in1.675s;2833 focused tests PASS in60.430s.
262 source pins /382 protected inputs; C234 training-AST parity PASS.
Six models x400 steps:2400 total steps /76800 answer presentations.
2454 model forwards /77664 total row presentations. All replays and changed-weight checks PASS.
Tracked tree clean; execution HEAD preserved; run_execution_valid=True.

Every one of12 seed/family/language cells: accuracy50% (4/8), fact-pair0/4, query-pair0/4,
evidence-mask drop0, query-mask drop0. full_probe_gate=False; gru_probe_gate=False.
This recipe did not fit even the selected16 seen TRAIN prompts. It does not prove architecture-wide
impossibility. Unchanged accuracy does not imply unchanged hidden activations or logits.

Acceptance/artifact identities: `docs/experiment-ledger-addendum-c236-c237.md`.
Acceptance record commit: `7b626b9a3886117145d3c469dc41549119d9a9ab`.
Do not rerun or rescue C236. No ability/generalization/core-superiority claim or Gate F promotion.

## Preserved earlier evidence

C235: diagnostic-integrity ACCEPTED PASS; all12 complete TRAIN cells below90%, accuracy47.9167%-53.125%.
Full evidence: docs/experiment-ledger-addendum-c235-c236.md.
Its initial invalid attempt remains in docs/experiment-ledger-addendum-c235-execution-recovery.md
and immutable log commit1615b5ce54afed8bde44ac9d326cace6c6e674d0.
C234: ACCEPTED VALID NEGATIVE; contextual binding not demonstrated on held-out value pairs.
Full evidence: docs/experiment-ledger-addendum-c234-c235.md.
C233 remains ACCEPTED VALID NEGATIVE; C232 remains bounded template-byte learning only.

## Next boundary

Prepare C237 as a frozen signal-path diagnostic of the accepted C236 checkpoints. Inspect paired
input/encoder/readout/logit changes separately from final argmax changes. No extra training,
checkpoint choice, architecture change or causal claim. Separate preregistration and independent
post-authoring review are required before activation.

## Numeric-memory track and stop

C230 route remains optional; numeric-memory tuning stays paused. Gate F is not waived.
Preserve accepted sources/tests/logs and tools/run_c167.ps1. No cleanup/history rewrite, paid API,
external corpus, larger model or production runtime change. Judge each C before its successor.
