# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C234 ACCEPTED VALID NEGATIVE. C235 ACTIVE / INVALID ATTEMPT RECOVERY. C236 NOT REGISTERED.**
C235 is the unique ACTIVE experiment. It is a frozen diagnostic, not a new capability gate.
The first attempt is INVALID; retry the same C235 after the reviewed test-only repair.
Current recovery post-authoring review is PASS; authoritative execution preflights remain mandatory.

## Current C235 execution recovery

Attempted execution HEAD: `d55e58f280bbd32776a6cd56ddc7507e6c827e1a`.
Published invalid-log commit: `1615b5ce54afed8bde44ac9d326cace6c6e674d0`.
Log SHA256: `37834dbd3572d43a94ccd2372f6bc070cd8ffae3745f69975e38fe82c25fafd5`.

Syntax and source/artifact prechecks passed. Own tests: 23 PASS / 1 FAIL out of24.
Test22 falsely rejected the word optimizer inside a result-limitation string in b.run.
The focused regression and scientific diagnostic were not started; run_execution_valid=False.
This is authoring failure, not evidence about binding ability. C234's verdict is unchanged.

Repair commit: `a972c32c4b3de5e58ad3d9d3c0f7734256bafce7`.
Only C235 test22 and its ast import changed. Executable AST is inspected instead of raw forbidden
substrings; a harmless-text fixture and11 prohibited-operation subtests guard the repair.
No test is removed. All24 test IDs, 2809 focused count, scientific code, model/data/seed/threshold,
manifest, workload, runner, launcher and accepted parent evidence remain unchanged.

Current recovery record, invalid evidence and review limitations:
`docs/experiment-ledger-addendum-c235-execution-recovery.md`.
This recovery record supersedes the initial readiness review; the original preregistration
continues to define the unchanged scientific conditions.

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

## C235 recovery post-authoring review

`post_authoring_review = PASS`

Review HEAD: `a972c32c4b3de5e58ad3d9d3c0f7734256bafce7`.
Scope: same-C test repair, remote source readback and targeted local verification; not formal C235.
The initial review at21fdd412 missed the source-string false positive and is superseded here.

Reviewed repaired test blob: `570711dbce5080fed307ac2c67d027d685a8a3d8`.
Unchanged benchmark blob: `12807b77a5f6bc36d185a931e54d651dcd557e39`.
Unchanged runner: `f6debab11f8fb88c3519752626d6f4512ae3297d`.
Unchanged launcher: `564359a1283a9bea333ce78611c085baa662d358`.

The committed test was re-fetched, and its Git blob identity matched locally tested bytes.
The original failing test was reproduced before repair; the repaired exact test passed against
actual unchanged b.run source, including harmless-text and11 forbidden-operation controls.
Full benchmark/test Python compile passed.17 fixture-independent test methods passed by direct
TestCase.run invocation; the parent dataset setUpClass was not run. The own loader still constructs
24 tests, and other test-method ASTs are unchanged. The ast import binding and unchanged manifest
hash were verified. No scientific, guard, test-count or protected-input condition is relaxed.

Reviewer environment: Python3.13.5 / PyTorch2.10.0+cpu / NumPy2.3.5.
The full24-test suite with parent fixtures,2809 focused tests, Windows PowerShell AST, accepted
local artifacts and36-forward diagnostic were NOT executed here. The container cannot clone the
full repo because github.com does not resolve. These checks remain mandatory in the unchanged
Windows launcher/runner and must not be reported as already passed.

Only recovery documentation changes after review HEAD. The final recovery documents are re-read
before returning the retry ExpectedHead. Do not reuse the old d55e58f2 execution HEAD.

## Numeric-memory track and stop

C230 prepared route remains optional; numeric-memory tuning stays paused.
Gate F is open, not waived.

Preserve all accepted sources/tests/logs and `tools/run_c167.ps1`.
No cleanup/history rewrite, larger model, paid API, external corpus, architecture change or new
training is part of C235.

Judge C235 before C236 registration.
