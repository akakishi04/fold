# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C232 ACCEPTED PASS. C233 ACTIVE / NOT YET JUDGED. C234 NOT REGISTERED.**
C233 is unique ACTIVE. Authoring is complete; do not execute before post-authoring review PASS.

## Accepted C232 — bounded bilingual learning

Scientific execution HEAD: `5fced21f02448e5b1047ef661186ce9b5c6bdb02`.
Published log commit: `3f67a03bdd5e5bc07e9324d8a7ea830ea798b7b7`.
Log SHA: `0c328cdc40d62bfee0523e685981e35327846f3124f7fee876839649eedaecf1`.
Summary SHA: `df75e3956a6bfaa37aaebdb12f3d189a10010576f0d9fa8709e5e399e1da75d2`.
Local summary:
`runs/c232-v5b-bilingual-learning-67b366b0db07449185a18bd0bbe7b996/summary.json`.
Validation SHA: `d7084ad67ee1072aa1c985c5d62ae958ce7771994db18bd29530442486e04ded`.
Measurements SHA: `ca14020688c9993edde9d176d596c7ffc1704ddbf78ab55520abbc48f5351c04`.
Checkpoint SHA: `c26e7bb71a9e9a882561165ef91e94b9c2ff257a0d39aa8166654c995e042a7b`.

Own32 tests OK in1.390s;2721/2721 focused tests OK in60.495s. Source/artifact/postchecks passed;
protected inputs preserved; tracked tree clean; run_execution_valid True. Only log/receipt published.
All three models completed400 steps each,1200 total and38400 TRAIN byte presentations.

| Seed | Final EN EVAL BPB | Final JA EVAL BPB |
|---:|---:|---:|
| 232001 | 0.541316849 | 0.524732128 |
| 232002 | 0.426583413 | 0.551531750 |
| 232003 | 0.479749709 | 0.448818815 |

All beat their own initialization and unigram EN4.579441272/JA4.642439365; TRAIN loss decreased.
Checkpoint fingerprints and48 short generation replays matched; reload error0. Verdict relies on
published evidence/local postchecks, not reviewer access to local-only checkpoints.
Acceptance record: docs/experiment-ledger-addendum-c232-c233.md (commit b0823af9f073c891ca6fa556c3bd93da0c2510cb).

This is learning on64 authored template sentences, not general language/reasoning. Four held-out
pairs and familiar vocabulary/grammar do not establish semantic composition. The learned GRU itself
may explain much of the improvement. C231 evaluator audit remains accepted. No complete v0.5,
learned-memory integration or Gate F completion is claimed.

## Active C233 — backbone-matched core ablation

Experiment C233-v5b-backbone-matched-core-ablation.
Stage V5-B-BACKBONE-MATCHED-CORE-ABLATION.

Question: under the same common initialization, TRAIN minibatches and400-step budget, does the
full C232 model beat a freshly trained GRU-only version with the iterative core removed?

Copy initial embedding/GRU/norm/decoder weights, not trained weights. Verify original full-model
initialization and restore accepted trained full checkpoints only for replay/comparison. Baseline
10160 parameters versus full13488; this is not a parameter- or compute-matched architecture contest.

Keep C232's64 sentences,48 TRAIN/948 bytes,16 EVAL/316 bytes and pair grouping. Reuse seeds
232001/232002/232003 and sample generator seed+1000 deliberately for pairing. CPU float64, threads2,
AdamW lr0.005, betas0.9/0.999, eps1e-8, weight_decay0, gradient clip1.0; batch32,400 steps per seed.
Only baseline trains:1200 new steps/38400 presentations, full retraining0. No EVAL tuning or early stop.

Qualify each baseline against its initialization/unigram first. Then full-core advantage requires
strictly lower full-model EVAL BPB in all six seed/language cells. Report both win counts and ties.
Unqualified baseline means INCONCLUSIVE, not evidence favoring full. Qualified gate misses are
valid negatives. Failed source/artifact/checkpoint replay is INVALID / RETRY SAME C233.
Same observed split is diagnostic reuse, not fresh confirmation. Capacity and recurrence effects
are not separated by a full-model win. No general language, speed or Gate F claim.

Parent238 sources/334 inputs + OWN6 and parent summary/artifacts ->244 sources/346 inputs.
Nine direct deciding dependencies. New tests32; modules118; loaded2754/focused2753; artifacts5.
Keep the inherited exact C204 mutable-state test exclusion only.
Manifest: `01459cd555cc15193b1289767cd824d159999faff130d537d16c5895f3f83d39`.
Registration: docs/experiment-ledger-addendum-c233-preregistration.md.
Design: docs/v5b-backbone-matched-core-ablation-v0.1.md.

## C233 post-authoring review

**post_authoring_review = PENDING**

The previous blocked test-file write was an authoring interruption. The standard create_file
operation subsequently succeeded (f1db06114d8b2e6beb6ff47a6807e3eb4b72584a). Runner/launcher/design/
preregistration are now present. No alternative write path was used. C232 rerun is unnecessary.
The original draft benchmark and scientific manifest remain unchanged.

Initial30 targeted tests passed in1.010s using real GRU/optimizer layers in synthetic parent
fixtures. Full-run adapter testing simulates training/evaluation and preserves a valid negative.
Pending locally: actual parent test31, historical test32/full2753 suite, Windows PowerShell AST,
accepted artifacts and formal baseline training. No claim these checks passed here.
Re-fetch committed code/test/runner/launcher, match tested blobs, rerun authoring tests and complete
source/loader/sampler/guard/protection review before issuing a command.

## Numeric-memory track and historical maintenance

C230 prepared route stays optional and numeric-memory tuning paused. Gate F is open, not waived.
No larger model, external data, paid API, new CI, cleanup, history rewrite or Actions-storage work.
Preserve all accepted sources/tests and tools/run_c167.ps1. Previous interruption record remains at
342c1afcae1f7447315843a2949c769a3f0b3c84:docs/experiment-ledger-and-handoff.md.

## Stop condition

After review PASS:32 own tests ->2753 focused tests ->C233 baseline training/comparison.
Judge C233 before C234 registration. Gate F remains NOT PASSED.
