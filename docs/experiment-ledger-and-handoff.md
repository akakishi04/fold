# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C234 ACCEPTED VALID NEGATIVE. C235 ACTIVE / NOT YET JUDGED. C236 NOT REGISTERED.**
C235 is the unique ACTIVE experiment. It is a frozen diagnostic, not a new capability gate.
Post-authoring review is PASS; authoritative execution preflights remain mandatory.

## Accepted C234 — contextual binding not established

Experiment: C234-v5b-contextual-binding-pilot.
Stage: V5-B-CONTEXTUAL-BINDING-PILOT.

Scientific execution HEAD:
`c225c2d82636085e2d639878738e1b9a7aa37b42`.

Published log commit:
`930fa77881d60558b3199b980f139ddef8bcb6ee`.

Log SHA:
`414e2de1fafa2fe86fb84bdc18a9477100086133df938a10b0244ad446e38de8`.

Summary SHA:
`a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523`.

Local summary:
`runs/c234-v5b-context-binding-fb381b067fc54cb3a46dbf3897ece200/summary.json`.

C234 execution validity is accepted:
-32 own tests PASS in2.037s;
-2785 focused tests PASS in50.439s;
-six models x400 steps =2400 training steps;
-76800 answer presentations;
-all checkpoint/prediction replays PASS;
-all weights changed;
-protected inputs preserved;
-clean tracked tree and preserved execution HEAD;
-`run_execution_valid = True`.

Scientific result is a valid negative:
`status = FAIL`, `full_binding_gate = False`, `gru_binding_gate = False`.

Exact EVAL correct answers:

| Seed | Full EN | Full JA | GRU-only EN | GRU-only JA |
|---:|---:|---:|---:|---:|
|234001|24/96|25/96|31/96|37/96|
|234002|24/96|24/96|39/96|36/96|
|234003|19/96|19/96|30/96|33/96|

Registered exact-accuracy threshold was90% in every seed/language cell.
Full query-pair both-correct: EN0/48 in all seeds; JA2/48 only for234001, otherwise0/48.
GRU-only query-pair both-correct:0/48 in every seed/language cell.
The other registered pair and masking criteria also failed.

Do not rerun C234, choose favorable seeds, extend steps or relax the gate.
The result does not prove architecture-wide impossibility, statistical equivalence, or general
language failure. It establishes only that contextual object/value binding was not demonstrated by
either fixed architecture under the registered C234 task and budget.

Acceptance:
`docs/experiment-ledger-addendum-c234-c235.md`.
Acceptance commit:
`8a58594d7fb4523ab2f5ef172d16cf7cafb7f4d1`.

Accepted artifacts:
- binding-plan.json `0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38`
- dataset.json `72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85`
- measurements.json `23f822d0a05faac176efc767b5702a21763946b295a76c503f01abc965c776c3`
- trained-models.pt `711dd636597d5ec575136bd780ac303eb21ed6198d411f977bb20c67fd20bd26`
- validation-summary.json `655dc04bd3509246c432eb8817699b5685ca300df612515d55358d78e634b629`

C233 remains ACCEPTED VALID NEGATIVE and C232 remains the bounded template-byte learning result.
Neither is rewritten by C234.

## Active C235 — frozen C234 TRAIN/EVAL binding diagnostic

Experiment: C235-v5b-frozen-binding-diagnostic.
Stage: V5-B-FROZEN-BINDING-DIAGNOSTIC.

One question:
with all six accepted C234 step400 checkpoints frozen, is failure already present on the complete
TRAIN set, or is there a descriptive gap between TRAIN and the held-out value-pair EVAL split?

Changed:
only evaluation coverage. Score complete TRAIN384 and EVAL192.

Held constant:
-C234 dataset/split/prompts/targets;
-all six final checkpoints and serialized identity order;
-full/GRU architectures and parameters;
-normal/evidence-blind/query-blind views;
-unconstrained byte scoring;
-CPU float64, threads2, deterministic algorithms;
-no new training or checkpoint selection.

For each split reuse C234 accuracy/NLL/pair/mask metrics. Also report supplied-value selection,
probability mass on supplied values, first/last-fact agreement, query-pair unchanged-answer rate and
query-pair both-correct count.

Diagnostic localization per seed/family/language uses the inherited90% exact-accuracy reference:
-`TRAIN_ACCURACY_BELOW_90`;
-`TRAIN_AT_LEAST_90_EVAL_BELOW_90`;
-`BOTH_ACCURACIES_AT_LEAST_90`.

These labels are descriptive only and cannot retroactively change C234.

Fixed workload:
-six models;
-two splits;
-three views;
-36 model forward calls;
-10368 rows presented across forwards;
-0 new training steps;
-0 optimizer steps;
-0 checkpoint writes;
-0 network calls.

C235 PASS means diagnostic integrity only:
accepted EVAL predictions/metrics replay, fingerprints unchanged, fixed workload complete and all12
diagnostic cells present. Accuracy outcome does not control C235 PASS. Any artifact/schema/replay/
nonfinite/model-mutation/source-protection fault is INVALID / RETRY SAME C235.

Protection:
256 source pins /370 protected inputs.
OWN6. Direct dependencies11.
New tests24; modules120; loaded2810/focused2809 with the inherited exact exclusion1.
Artifacts5: diagnostic-plan.json, diagnostics.json, predictions.json, model-fingerprints.json,
validation-summary.json.
Manifest SHA:
`2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3`.

Design:
`docs/v5b-frozen-binding-diagnostic-v0.1.md`.
Registration:
`docs/experiment-ledger-addendum-c235-preregistration.md`.

## C235 post-authoring review

`post_authoring_review = PASS`

Review HEAD: `21fdd412a95d9c4f024dc92c20a4dc17d3d6f955`.
Scope: committed remote source/static contract review, not formal diagnostic execution.

Remote blobs at review HEAD:
benchmark `12807b77a5f6bc36d185a931e54d651dcd557e39`;
tests `2c880ae9b35a214d7a7e0425c5c674fad10027d3`;
runner `f6debab11f8fb88c3519752626d6f4512ae3297d`;
launcher `564359a1283a9bea333ce78611c085baa662d358`.

Acceptance-to-review comparison changes only C235 OWN6 plus this handoff. Static audit confirms:
no C235 fit/optimizer/torch.save path; frozen model fingerprints are checked; parent EVAL is replayed;
36 forwards/10368 rows/0 training are fixed;24 test methods are present; runner registers
2810 loaded/2809 focused tests and three precheck/regression/postcheck blocks; launcher resolves only
ACTIVE C235 and requires clean tree/exact HEAD/parser success before execution/publication.
Independent manifest reconstruction matched
`2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3`.

Reviewer-local execution was not possible because the isolated environment could not resolve
github.com for a clone. Python py_compile,24 authoring tests,2809 focused tests, Windows PowerShell
AST, local C234 artifact reads and the36-forward diagnostic remain authoritative runner preflights
and are not represented as already passed. Any defect stops C235 before a valid diagnostic result.

## Numeric-memory track and stop

C230 prepared route remains optional; numeric-memory tuning stays paused.
Gate F is open, not waived.

Preserve all accepted sources/tests/logs and `tools/run_c167.ps1`.
No cleanup/history rewrite, larger model, paid API, external corpus, architecture change or new
training is part of C235.

Judge C235 before C236 registration.
