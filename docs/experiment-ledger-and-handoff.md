# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C239 ACCEPTED VALID NEGATIVE. C240 NOT REGISTERED. C241 NOT REGISTERED.**
No active experiment during acceptance-to-registration transition.
C238 remains minimal seen-TRAIN fitting PASS; C237 remains diagnostic-integrity PASS only.

## Latest accepted evidence — C239

Scientific execution HEAD: c847609c8d045c9c5db4ec882bf336a9671180ff.
Published log commit: 5207d3b378ae56502a78dc9a5bb6f843cf389795.
Log SHA256:9e139f0544b49cb1185ce285a7b7c2c7ccb5ad394198040be4845648aa3697ee.
Summary SHA256:500af8c078c5a6114d1cb115b0dad9ee5ae7f622c41fce765f144668e2e041af.
Local summary:runs/c239-v5b-order-holdout-884d8453a9f348c3991109930cca2ca5/summary.json.

24 own tests PASS;2905 focused tests PASS.280 source pins/418 inputs protected.
2400 training steps/76800 answer presentations;2490 total forwards/77520 rows.
All replays/weight-update checks PASS;tracked tree clean;execution HEAD preserved;run_execution_valid=True.
All12 cells pass TRAIN:4/4 answers,2/2 fact/query pairs,0.50 mask drops.
All12 cells are ORDER_HOLDOUT_MISS:0/4 or1/4 answers,0/2 pairs,negative mask drops.
C239 learned the training order but did not transfer to the reversed order. No causal mechanism proved.

Acceptance/artifact details:docs/experiment-ledger-addendum-c239-c240.md.
Acceptance record commit:b739256640949f69a6ca781d31cde108cbe1edf6.
Published evidence/postcheck was checked;no reviewer checkpoint rerun or independent full-log rehash.
Do not rerun C239, alter thresholds or reinterpret C238 as a generalization result.

## Preserved earlier evidence

C238:all12 seen-TRAIN cells100%,both families pass after complete-cohort sampling.
Details:docs/experiment-ledger-addendum-c238-c239.md.
C237:internal numerical sensitivity without correct answer switching;diagnostic PASS.
C236:valid negative on the16 prompts with random replacement sampling.
C235:diagnostic PASS;failure already on complete TRAIN;first INVALID attempt remains preserved.
C234/C233 remain valid negatives;C232 remains bounded template-byte learning only.

## Next boundary

Prepare C240 as an analysis of saved C239 predictions against explicit positional/identity/constant
rules, with discrete-metric replay, paired order comparisons and out-of-value-byte counts.
No new inference, training, checkpoint load/write or capability claim. A rule match is not proof of
an internal algorithm;binary-rule degeneracies must be reported. Separate preregistration and
remote-readback authoring review are required before activation.

## Stop and scope

Gate F NOT PASSED;numeric-memory tuning paused. Preserve accepted sources/tests/logs and
tools/run_c167.ps1. No cleanup/history rewrite,paid API,external corpus,larger model or production change.
Judge each C before registering its successor.
