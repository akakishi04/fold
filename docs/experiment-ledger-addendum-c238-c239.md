# C238 acceptance and C239 order-holdout boundary

## Formal verdict

**C238 ACCEPTED PASS — minimal seen-TRAIN fitting only.**
Full and GRU-only both meet every preregistered criterion in every seed/language cell.
C236 remains ACCEPTED VALID NEGATIVE; C237 remains diagnostic-integrity PASS only.
Gate E PASSED; Gate F NOT PASSED. No general-language or held-out-generalization claim.

Scientific execution HEAD: `a7999c92e2f6f071c045de268feaf5ddd6f438ac`.
Published log commit: `93a86ea4493c4c6bf20b046b56c29e8bccc322f9`.
Publisher-recorded log SHA256: `da9386a9f351ebf9aeec18df7057aac9971c4b068fbe337efdcf7363260b8e60`.
Log bytes: 539013.
Summary SHA256: `06ab54549477894ea17f986364cacc6b3b7d25ff2dea70b18e98e2a957c80363`.
Local summary: `runs/c238-v5b-complete-cohort-sampler-df6538e306784434bdcbb2848e4c278d/summary.json`.

The published commit is one commit after execution and changes only c238/latest.log/latest.json.
Acceptance uses retrieved log ranges and their recorded user-local postcheck, not an independent
rerun of checkpoints or an independent full-log byte hash. The log and its original identity remain.

## Execution validity

24 own tests PASS in3.553s;2881 focused tests PASS in72.485s.
Python syntax, source/artifact and sampler-only training-AST checks PASS.
274 source pins /406 protected inputs. All6 models completed400 steps each:
2400 training steps /76800 answer presentations /2454 total model calls /77664 total rows.
Every initial-state replay, final checkpoint/prediction replay and weight-update check passed.
Recorded C236 comparator measurements remained unchanged. Postcheck preserved protected inputs,
clean tracked tree and execution HEAD. `run_execution_valid=True`.
`scientific_status=PASS`, `full_probe_gate=True`, `gru_probe_gate=True`.

## Deciding metrics

Every one of12 seed/family/language cells:
- exact accuracy8/8 (100%), versus C2364/8 (50%): +50 percentage points;
- fact-pair both-correct4/4 and query-pair both-correct4/4, versus C2360/4;
- evidence-mask drop0.50 and query-mask drop0.50, versus C2360;
- final normal answer NLL between0.000354 and0.001049 (logged six-decimal values).

The unchanged registered thresholds were accuracy>=0.90, each paired criterion>=0.80,
and each mask drop>=0.35. All criteria passed; no threshold, seed or endpoint was changed.

## Interpretation and limits

The tested architectures can fit this16-prompt set under complete-cohort updates without more
parameters or more updates. The claim that neither architecture can fit even this set under any
sampling recipe is contradicted by C238. C236's particular failed recipe remains valid evidence.

The registered change from random replacement batches to the complete cohort twice was sufficient
for the observed improvement at matched initial weights, optimizer and budget. It jointly changes
coverage, within-batch factor/label balance and gradient variability. It does not isolate which
of these mechanisms matters, establish a universal sampler advantage, or explain every past miss.
Both model families passed; this does not establish a Full/core-specific advantage.

These are the same16 prompts used in training. Prompt memorization is not excluded. Mask sensitivity
and paired correctness do not by themselves establish transfer to unseen prompts, new entities,
new values, general language, memory, causal reasoning or Gate F completion.

## Accepted artifacts

- measurements.json: `3d358412484f9f9d227ea0a37e8b5ca9de72fff980f8f7d0d32a95982b658fe7` (12333 bytes)
- probe-dataset.json: `bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c` (2654 bytes)
- sampler-plan.json: `ae9d0b7e92ee7024b57210f1779aebbfc0757fa995acbdf6f9359b2f23664232` (2776 bytes)
- trained-models.pt: `2a09b28dd2a10c210380cbe05eb18360f69d309e44bc3e9599f0eb3e178c624d` (601940 bytes)
- validation-summary.json: `8c7edfb3a5634bd06a7d3f4b15db909d7e09330e1cec844bda943a363f69670a` (385 bytes)

## Next question — unseen fact-order transfer

Can freshly initialized models trained only on order0 prompts (box then book;8 rows) answer the
otherwise matched order1 prompts (book then box;8 rows), without those strings entering training?
The same underlying assignments and questions are intentionally shared; exact prompts and row IDs
are held out. This is order-transfer, not a disjoint-fact/entity/value test.

Use the fixed16-row pool, fresh initial states, same architectures/optimizer/400-step budget, and
complete-cohort batch32 (the8 training rows repeated4 times). Holdout rows are scored only after
step400 and checkpoint replay; they never enter the optimizer, early stopping or selection.
Never initialize from C238 trained states, which have already seen both orders.

This changes training coverage and evaluation split, not a single matched C238 performance endpoint.
Repetitions per retained row increase from800 to1600 as a consequence of the restricted cohort.
A pass is limited order transfer; a valid miss is reported separately from a TRAIN-fit miss.
This acceptance record does not register C239. Separate preregistration and post-authoring review
control activation. Numeric-memory tuning stays paused; no C240 before C239 judgment.
