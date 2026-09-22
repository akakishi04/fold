# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C232 ACCEPTED PASS. C233 NOT REGISTERED. C234 NOT REGISTERED.**

There is no ACTIVE experiment. C233 authoring is incomplete following a blocked connector write.
Do not execute the draft benchmark or reuse the previous C232 command as a new experiment.

## Accepted C232 — bounded bilingual learning

Scientific execution HEAD: `5fced21f02448e5b1047ef661186ce9b5c6bdb02`.
Published log commit: `3f67a03bdd5e5bc07e9324d8a7ea830ea798b7b7`.
Log SHA256: `0c328cdc40d62bfee0523e685981e35327846f3124f7fee876839649eedaecf1`.
Summary SHA256: `df75e3956a6bfaa37aaebdb12f3d189a10010576f0d9fa8709e5e399e1da75d2`.
Local summary:
`runs/c232-v5b-bilingual-learning-67b366b0db07449185a18bd0bbe7b996/summary.json`.
Validation SHA: `d7084ad67ee1072aa1c985c5d62ae958ce7771994db18bd29530442486e04ded`.
Measurements SHA: `ca14020688c9993edde9d176d596c7ffc1704ddbf78ab55520abbc48f5351c04`.
Checkpoint SHA: `c26e7bb71a9e9a882561165ef91e94b9c2ff257a0d39aa8166654c995e042a7b`.

Own32 tests OK in1.390s;2721/2721 focused tests OK in60.495s. Source/artifact prechecks and final
postchecks passed; protected inputs preserved; tracked tree clean; run_execution_valid True.
Publication changed only the log and receipt. Verdict uses published evidence and recorded local
postchecks, not reviewer access to user-local checkpoints.

All three13488-parameter models completed400 steps each,1200 total and38400 TRAIN byte presentations.
Every seed lowered TRAIN BPB and beat its own initialization and the TRAIN-only unigram on EVAL,
separately in English and Japanese.

| Seed | Initial EN | Final EN | Initial JA | Final JA |
|---:|---:|---:|---:|---:|
| 232001 | 8.139344152 | 0.541316849 | 8.656696136 | 0.524732128 |
| 232002 | 8.127756147 | 0.426583413 | 8.573135698 | 0.551531750 |
| 232003 | 8.243823111 | 0.479749709 | 7.797179309 | 0.448818815 |

Unigram EVAL BPB: EN4.579441272 /JA4.642439365. All checkpoint fingerprints round-tripped,
EVAL reload error0, all48 short generation replays exact. Weights actually changed.
Full acceptance record: docs/experiment-ledger-addendum-c232-c233.md.

### Meaning and limits

This is actual byte-pattern learning on64 authored template sentences, not general language or
reasoning competence. TRAIN48 sentences/12 pairs; EVAL16 sentences/four pairs; vocabulary/templates
seen in TRAIN. Low teacher-forced BPB can reflect spelling/format learning. Generation was a
four-byte replay check, not a semantic task. The GRU front-end is itself learned; beating a unigram
does not establish a contribution unique to the FOLD core.

C231's evaluator audit remains accepted. The model is the fixed-slot, fixed-route uncompressed V5-B
reference, not a complete v0.5 system or the integrated learned-memory stack.

## Proposed C233 — incomplete authoring, not execution permission

Question: with the same initial embedding/GRU/norm/decoder, TRAIN rows, sampled minibatches and
400-step budget, does the full C232 model outperform a newly trained version with the iterative
fixed-routing core removed?

The intended baseline is GRU-only:10160 parameters versus13488 total in the full model. This is a
backbone-matched capacity-reducing ablation, not a parameter/compute-matched architecture contest.
Copy initial common weights, not trained weights. Restore accepted C232 full checkpoints only for
replay/comparison. Reuse seeds232001/232002/232003 deliberately for matched initializations and
sample order. No new full-model training or EVAL-based tuning. The already observed C232 split is
a diagnostic reuse, not independent confirmation.

Draft intended gate: qualify baseline learning against its own initialization/unigram, then require
full-model BPB strictly lower in all six seed/language cells. A competitive smaller ablation weakens
necessity on this task; a full-model win does not separate added capacity from iterative structure.
An unqualified baseline is inconclusive for superiority, not evidence favoring the full model.

### Authoring stop and exact repository state

Acceptance document committed at `b0823af9f073c891ca6fa556c3bd93da0c2510cb`.
Draft benchmark added at `2f6ef6d38b85710742a8256b0123e36ff5c975c9`:
`fold_lm/v05_benchmarks/model_c233_core_ablation.py`.

The attempt to create `tests_lm/test_v05_c233_core_ablation.py` was blocked by the tool safety check.
No successful test-file write was returned and branch HEAD did not advance. Do not treat the tests,
runner, launcher or C233 preregistration as committed. No alternative write route was attempted.
C233 has not been activated and has not passed committed-remote post-authoring review.

Local authoring copies of benchmark/tests/runner/launcher were prepared.30 targeted tests passed
using real GRU/optimizer layers in a synthetic source container; the full-run adapter simulated
training and preserved a valid negative. These are not the real parent test, full historical
regression, accepted-checkpoint comparison or a completed remote review. They do not authorize a run.

Before any future C233 registration, resolve the blocked authoring step through the permitted tool
workflow, complete all OWN files and review the committed remote sources. Recheck source/protection
counts, manifest, parent artifact semantics, sampler/initialization matching, runner/launcher guards
and actual test counts. Never infer execution readiness from the draft benchmark alone.

## Numeric-memory track and historical maintenance

C230 improved original H1/H2 time but lost to the strong full-factor comparator in11/12 cells; its
only stream-time advantage disappeared after setup. Keep the prepared route optional and pause
numeric-memory tuning. Gate F is open, not waived. No larger model budget, external data, paid API,
new CI, cleanup, history rewrite or Actions-storage change is authorized by this work.

Earlier detailed handoff:
`3f67a03bdd5e5bc07e9324d8a7ea830ea798b7b7:docs/experiment-ledger-and-handoff.md`.
Preserve all accepted sources/tests and tools/run_c167.ps1.

## Stop condition

C232 is closed as ACCEPTED PASS. C233 remains NOT REGISTERED; no run command is authorized.
Do not register C234. Gate F remains NOT PASSED.
