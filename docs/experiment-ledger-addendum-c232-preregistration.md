# C232 preregistration — grouped bilingual learning pilot

**C231 ACCEPTED PASS. C232 ACTIVE / NOT YET JUDGED. C233 NOT REGISTERED.**
V5-B bounded learning pilot. Gate E PASSED; Gate F NOT PASSED. No V5-G promotion.

## One scientific question

Does400-step training of the unchanged C231 V5-B model reduce held-out noun/color-combination
byte loss versus its own initialization and a TRAIN-only smoothed unigram, in both languages?

Changed variable: weights trained on a registered authored corpus. Model architecture, float64
precision, fixed routing, prefix-boundary EOS and next-byte scoring remain the C231 reference.
No learned memory integration, compression changes, general benchmark or new runtime architecture.

## Accepted parent identity

Execution HEAD: `06a1b674d58f16816a3f47ec36dc3843e7e1dc37`.
Published log commit: `429cb50b326e2013503058c9cebd3468654e73ba`.
Summary SHA256: `53f9c163beeeab1617eb8946e902cb29c2bbc4a94fb869d3325381160107b522`.
Validation SHA256: `316435e0a31e0559a73368171df186336852990f16e4aa55b322e776ba281938`.
Local summary: `runs/c231-v5b-byte-eval-9e4c4cd1513a4b3c97e598252f6300c5/summary.json`.

C231 parent source count232, protected input count322. Validate its summary, all five artifacts,
all accepted sources and protected files. Its saved checkpoints are untrained instrument models;
C232 does not mislabel them as trained models or resume them. Instantiate new fixed C232 seeds
through the accepted C231 factory instead. All import/model/helper sources are inherited unchanged.

## Fixed corpus and split

Two languages x4 nouns x4 colors x2 templates =64 authored sentences.
EVAL iff (noun_id+color_id)%4==0. Pair is the grouping unit across all languages/templates.
TRAIN48 sentences/12 pairs/948 bytes (en492,ja456).
EVAL16 sentences/4 pairs/316 bytes (en164,ja152).
No pair or exact sentence crosses splits; all vocabulary and templates appear in TRAIN.

Data SHA256: `1a1b09c80c3877c662ee43bf91fb00b7a762d20a7b6b3f455f5ee208c7a79200`.
Rendered sentences and split metadata are stored in local-only dataset.json.
Detailed templates and meaning: docs/v5b-grouped-bilingual-learning-v0.1.md.

Reuse C231.document_rows to create observed-prefix-only48-slot examples with separate real-byte
targets. No random prefix-row split, special-token loss, future target input or UTF-8 truncation.
fit() receives TRAIN tokens/targets only. Language metadata is used by scoring and the unigram,
not as an extra neural input.

## Fixed training and references

Seeds232001/232002/232003. Model13488 total parameters, width16,2 modules,2 internal steps,
TASK_NEXT=0. CPU float64, threads2, deterministic algorithms.
AdamW lr0.005, betas0.9/0.999, eps1e-8, weight_decay0. Gradient L2 clipping1.0.
400 steps/seed; batch32; uniform TRAIN byte-row sampling with replacement, generator seed+1000.
Total1200 steps and38400 byte presentations. Final step400 only, no early stopping or EVAL-based
checkpoint/seed/hyperparameter selection. Printing training loss is monitoring, not budget control.

Score before/after TRAIN and EVAL with byte-weighted NLL and BPB overall and per language.
Unigram references are per-language TRAIN-only byte counts with add-one smoothing over256 values.
They are calibration baselines, not a matched neural comparison or proof of FOLD-specific benefit.

## Fixed learning gate

Every seed must satisfy:
- final aggregate TRAIN BPB strictly below its own initial TRAIN BPB;
- final English EVAL BPB strictly below both initial English EVAL BPB and English unigram EVAL BPB;
- same two strict comparisons for Japanese EVAL;
- weights changed; trained checkpoint fingerprint roundtrip exact;
- EVAL logit reload error <=1e-9;
- all16 four-byte greedy continuations reproduce after reload.

No100% byte accuracy/fluency criterion. Short generated hex outputs are descriptive. Loss gains can
reflect spelling/format learning, not semantic understanding. These16 held-out sentences are four
underlying pairs with four realizations, not16 independent semantic tasks. Three seeds do not
multiply the number of independent data points. No general-language or Gate F claim.

A finite complete run missing the learning gate is scientific FAIL / valid negative. Do not add
steps, change the split, relax comparisons or replace a failed seed after viewing it. Source,
artifact, runner, malformed/nonfinite output or incomplete training defects are INVALID / RETRY
SAME C232. Output validation and postcheck permit a complete valid negative to be serialized.

## Authoring and protection

OWN6:
- fold_lm/v05_benchmarks/model_c232_bilingual_learning.py
- tests_lm/test_v05_c232_bilingual_learning.py
- tools/run_c232.ps1
- tools/invoke_c232.ps1
- this preregistration
- docs/v5b-grouped-bilingual-learning-v0.1.md

232 parent sources +6 new =238.322 inputs +6 parent summary/artifacts +6 new source files =334.
Direct scientific dependency checks include the five C231 LM/import pins, C231 evaluator/model
factory, C230 audit-helper entry and the new benchmark; all transitive parent helpers stay pinned.
No accepted historical source/test is changed. New tests32; modules117; loaded2722/focused2721.
Only the inherited exact historical exclusion remains:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Artifacts5: learning-plan.json, dataset.json, trained-models.pt, measurements.json,
validation-summary.json. All outputs/checkpoints stay ignored under runs/. Only console/receipt
are mirrored to docs/experiment-run-logs/c232/ by the existing publisher.

Manifest SHA256: `09f2a463981d49680ca66940698baf363731adda9fda8718c5b59fdc281b80c4`.

## Post-authoring review

`post_authoring_review = PASS`

Review HEAD: `2c8a97bb56a3eb79aebea556c04bbdf49d374af1`.
Scope: committed-source audit and targeted synthetic authoring validation, not formal science.

All four committed code/test/PowerShell files were re-fetched after authoring and their Git blob
identities matched the tested local copies exactly:

| File | Blob |
|---|---|
| C232 benchmark | 644f7cd3b1d89454f33be1431616a655f8d215db |
| C232 tests | cb72903208ed62c485654491ec9a051e4fe3a244 |
| run_c232.ps1 | 8dc24a77e78236cd79325a1417fd1f8baefd3767 |
| invoke_c232.ps1 | b315131db009489ff762dbda244f6a4c09813b21 |

After comparison30 tests reran:30 PASS,0 failures/errors in0.062s, Python3.13.5 /
PyTorch2.10.0+cpu / NumPy2.3.5.32 methods enumerated. Both Python sources and all three embedded
runner Python blocks compiled; unresolved global names0 (including legitimate interpreter-injected
module globals in the analysis). Data/manifest hashes recomputed exactly. Dataset48/16 split,
948/316 byte counts, pair-group isolation, TRAIN-only unigram, byte-weighted scoring and no EVAL
arguments to fit() were checked. Actual optimizer tests performed two synthetic steps; the full-run
adapter deliberately simulated training and verified a valid negative, outputs and postchecks.
Neither fixture is claimed as400-step learning or actual V5-B evidence. No EVAL-driven tuning.

Source review checked parent artifact identities/semantics, model factory and prefix adapter reuse,
238/334 protection accounting, direct dependency coverage, CLI precheck[1]/postcheck[1..3], exact
source-string assertions, early own-test ordering and complete parser/ACTIVE/HEAD/publication guards.
Git comparison from the C231 log commit shows only new files and the unpinned handoff. No accepted
source, test, log or dependency was edited/deleted. C233 remains unregistered.

Not executed here: test31 actual V5-B TRAIN-only two-step smoke, test32/full2721 historical suite,
Windows PowerShell AST parsing, user-local accepted-artifact checks or formal1200-step C232 run.
The container could not resolve raw.githubusercontent.com; connector reads worked. Synthetic tests
are not substitutes for those checks. The authoritative runner executes all32 new tests, then2721
focused tests, then fixed-budget science; failure stops and publishes evidence. Review PASS does
not claim the pending checks ran. After the review HEAD only review documentation changes.

## Stop

Run32 new tests,2721 focused tests, then the fixed-budget pilot. Judge C232 before C233 registration.
No numeric-memory tuning, larger model, external data download, paid API, CI addition or cleanup.
