# V5-B backbone-matched core ablation v0.1

## Single question

Under the same initial byte embedding, GRU, readout normalization and decoder, the same TRAIN
minibatches and the same400-step budget, does the full C232 model achieve lower held-out byte loss
than a separately trained GRU-only model with the iterative core removed?

C232 established learning relative to initialization and a weak unigram. This experiment isolates
whether that task needs the added core, rather than attributing the learned GRU's success to it.
It is an exploratory diagnostic on the already observed C232 split, not a fresh confirmation.

## Changed and fixed

Remove only the fixed-routing iterative core from the newly trained comparison model:

```text
Full:     embedding -> GRU -> iterative core -> normalization -> decoder
Ablation: embedding -> GRU -----------------> normalization -> decoder
```

The baseline copies INITIAL common weights before the full model receives its accepted trained
checkpoint. Copies have independent storage. No trained full weights are used to initialize the
baseline. No dormant core parameters remain in the baseline.

Full13488 parameters, GRU-only10160. This is a backbone-matched, capacity-reducing ablation, not a
parameter-matched or compute-matched architecture contest. Gradient clipping uses the same global
norm threshold but operates on different parameter sets, so optimization geometry is not identical.
The unchanged hyperparameter recipe is a bounded diagnostic, not optimal tuning for each model.

Reuse C232's exact64 sentences and grouped split:48 TRAIN sentences/948 bytes,16 EVAL sentences/316
bytes, with noun/color pairs held together across both languages and templates. No new vocabulary,
syntax or semantic task is introduced. Reuse C231's observed-prefix-only48-slot adapter and byte
likelihood evaluator. NEXT route is fixed; no controller or learned memory is integrated.

## Parent evidence and pairing

Load the accepted C232 trained-models.pt and measurements.json through explicit schema/metric
adapters. Reconstruct each original initialization using C231.new_model and verify its fingerprint
before copying common weights. Then restore the full trained state and replay EVAL metrics and the
16 four-byte generation records. Replay is execution validity, not the new scientific intervention.

Seeds232001/232002/232003 are reused deliberately for pairing, not selected for new performance.
The TRAIN-only CPU sampler uses seed+1000 exactly as in C232. Data ordering and draws are unchanged.
The full model is not retrained. Only the three GRU-only baselines train400 steps each.

## Budget

CPU float64, threads2, deterministic algorithms. AdamW lr0.005, betas0.9/0.999, eps1e-8,
weight_decay0. Gradient norm clipping1.0. Batch32, TRAIN byte rows sampled with replacement.
Total1200 new steps /38400 byte presentations. No early stopping, larger budget, failed-seed
replacement or EVAL-based checkpoint/hyperparameter selection. Final step400 only.

## Fixed interpretation

First qualify the baseline: every seed must lower aggregate TRAIN BPB and beat its own initial
EVAL BPB and TRAIN-only add-one unigram separately in English and Japanese. A baseline failing
qualification makes the superiority comparison INCONCLUSIVE; it does not favor the full model.

Then compute six cells: three seeds x two languages. Delta is full BPB minus GRU-only BPB.
Negative delta favors full; positive favors the baseline; exact zero is a tie.
The registered full-core advantage gate requires all six deltas strictly negative with a qualified
baseline and successful replay. Ties do not satisfy that gate.

A full win supports contribution on this task only, not whether recurrence or extra capacity caused
it. A competitive smaller model weakens necessity on this pilot but does not refute FOLD generally.
Finite complete gate misses are valid negatives. Invalid source/artifacts, malformed/nonfinite
results or failed checkpoint replay stop as INVALID / RETRY SAME C233. Never weaken gates after
observing the result. No general language, efficiency or Gate F claim.

## Execution

The active dispatcher invokes the guarded C233 launcher.32 new tests precede2753 focused tests,
then baseline training. Console progress is printed every100 steps. All generated artifacts remain
local-only under ignored runs/; the normal publisher mirrors only console text and its receipt.

Output artifacts: comparison-plan.json, baseline-models.pt, comparisons.json, replay-audit.json,
validation-summary.json, plus summary.json. Counts:244 source pins and346 protected inputs.
Source dependencies, parent identity and unchanged scientific manifest are fixed in preregistration.

C233 follows the same registered question as the interrupted draft. The previous connector block
was an authoring interruption, not a failed scientific run. No C232 rerun or next C234 is needed.
