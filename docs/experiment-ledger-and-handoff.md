# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository akakishi04/fold; branch feat/sft-target-loss; local M:\asobiba\fold.
Authoritative runtime: Python3.13.15 / PyTorch2.10.0+cu130 / NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.

**C231 ACCEPTED PASS. C232 ACTIVE / NOT YET JUDGED. C233 NOT REGISTERED.**
C232 is unique ACTIVE. Source review passed; all execution preflights remain mandatory.

## Accepted C231 — evaluation instrument only

Execution HEAD: `06a1b674d58f16816a3f47ec36dc3843e7e1dc37`.
Published log commit: `429cb50b326e2013503058c9cebd3468654e73ba`.
Log SHA256: `d3573869fa797567ff2542941f1286a11e9d15b27b0966ed63c9a11d43b13fea`.
Summary SHA256: `53f9c163beeeab1617eb8946e902cb29c2bbc4a94fb869d3325381160107b522`.
Validation SHA256: `316435e0a31e0559a73368171df186336852990f16e4aa55b322e776ba281938`.
Local summary: `runs/c231-v5b-byte-eval-9e4c4cd1513a4b3c97e598252f6300c5/summary.json`.

Own24 tests OK in1.443s;2689/2689 focused tests OK in56.379s.232 source pins/322 protected inputs.
All input/artifact/replay/postchecks passed; tracked tree clean; run_execution_valid True.
Three untrained13488-parameter V5-B instruments,378 forwards,246 scored byte positions.
Maximum batch/singleton drift1.3322676295501878e-15; scoring drift1.7763568394002505e-15.
Suffix and checkpoint reload drift0; all12 short generation replays exact; no weight changes/training.
Verdict uses published evidence and local postchecks, not reviewer access to local-only artifacts.
Full record: docs/experiment-ledger-addendum-c231-c232.md.

C231 established prefix-only evaluation mechanics, not language skill. Four authored texts and
random-model scores do not establish understanding, useful generation or whole-model performance.
The model is the fixed-slot, teacher-routed uncompressed V5-B reference, not the legacy model or
an integrated final v0.5 system. Prefix-boundary EOS is an explicit adapter convention.

## Numeric-memory track decision remains fixed

C230 improved original H1/H2 update+query time by about32%-55%, but lost to full-factor reuse in11/12
cells. Its only stream-time win disappeared when setup was included. Keep prepared_capsule as an
opt-in CPU-float64 fixed-W candidate; do not change default/reference or pursue more favorable
numeric workloads here. Gate F remains open, not waived. The accepted semantic/safety pilots and
all scientific source pins remain intact. Details: docs/experiment-ledger-addendum-c230-c231.md.

## Active C232 — grouped bilingual learning pilot

Experiment C232-v5b-grouped-bilingual-learning-pilot.
Stage V5-B-GROUPED-BILINGUAL-LEARNING-PILOT.

One question: does a fixed400-step budget improve held-out noun/color-combination byte prediction
versus the same model's initialization and TRAIN-only unigram references in both English/Japanese?

Use unchanged C231.new_model:13488 parameters, width16,48 slots,2 modules/2 internal steps,
fixed TASK_NEXT=0, CPU float64. Fresh seeds232001/232002/232003; no C231 checkpoint continuation.
No memory/compression/controller integration, new architecture, general benchmark or V5-G promotion.

64 authored sentences =2 languages x4 nouns x4 colors x2 templates.
EVAL iff (noun_id+color_id)%4==0, with the pair grouped across all languages/templates.
TRAIN48 sentences/12 pairs/948 bytes; EVAL16 sentences/4 pairs/316 bytes.
All vocabulary/templates occur in TRAIN. Next-byte targets stay outside the model input.

AdamW lr0.005, betas0.9/0.999, eps1e-8, weight_decay0, clip norm1.0, batch32.
400 steps per seed;1200 total;38400 sampled TRAIN byte presentations. No early stopping or EVAL-based
checkpoint/seed/budget selection. fit() receives only TRAIN tokens/targets; unigram counts TRAIN only.

Fixed gate, every seed: aggregate TRAIN BPB decreases; final English EVAL BPB below initial and
unigram; same for Japanese; changed weights; exact checkpoint fingerprints, logit replay <=1e-9,
and all16 four-byte generation replays exact. These are limited byte-pattern results, not proof of
semantic composition or useful language competence. Unigram is not a matched neural baseline.
Complete finite gate misses are valid negatives and must not trigger threshold/budget relaxation.

Parent232 sources/322 inputs -> C232238 sources/334 inputs; OWN6; artifacts5.
New tests32; modules117; loaded2722/focused2721 with inherited exact exclusion1.
Data SHA: `1a1b09c80c3877c662ee43bf91fb00b7a762d20a7b6b3f455f5ee208c7a79200`.
Manifest SHA: `09f2a463981d49680ca66940698baf363731adda9fda8718c5b59fdc281b80c4`.
Registration: docs/experiment-ledger-addendum-c232-preregistration.md.
Design: docs/v5b-grouped-bilingual-learning-v0.1.md.

## C232 post-authoring review

**post_authoring_review = PASS**

Review HEAD: `2c8a97bb56a3eb79aebea556c04bbdf49d374af1`.
Scope: committed-source audit and targeted synthetic authoring validation, not formal science.

Four re-fetched code/test/PowerShell blobs matched tested copies. After comparison30 tests reran:
30 PASS,0 failures/errors,0.062s on Python3.13.5 / PyTorch2.10.0+cpu / NumPy2.3.5.32 methods enumerated;
both Python sources and three embedded runner blocks compiled; unresolved globals0; data/manifest
hashes matched. Dataset/grouping/TRAIN-only unigram and fit inputs, byte-weighted scoring, two-step
synthetic optimizer updates, fixed workload and valid-negative output paths were checked. Full-run
adapter testing simulated fit and is not a formal V5-B training result. No held-out quality tuning.

Source review checked parent artifact/model-factory/prefix semantics,238/334 dependency protection,
CLI precheck[1]/postcheck[1..3], exact source-string assertions, early tests and complete launcher
parser/ACTIVE/HEAD/publication guards. Git compare shows only new files plus the unpinned handoff;
no accepted scientific sources/tests/logs/dependencies were changed. C233 remains unregistered.

Not run here: test31 actual TRAIN-only two-step V5-B smoke, test32/full2721 historical suite,
Windows PowerShell AST, user-local parent artifacts or formal1200-step training. Synthetic fixtures
are not represented as these checks. Runner requires32 own tests and2721 focused tests before
science; failures stop and publish evidence. Only review documentation changes after the review HEAD.

## Historical maintenance and stop

Prior handoff:429cb50b326e2013503058c9cebd3468654e73ba:docs/experiment-ledger-and-handoff.md.
Preserve all accepted sources/tests and tools/run_c167.ps1. No cleanup/history rewrite/new CI or
Actions-storage work. Run32 own tests,2721 focused tests, then fixed-budget C232. Judge it before
C233 registration. No large-model budget or public-data download is authorized by this pilot.
