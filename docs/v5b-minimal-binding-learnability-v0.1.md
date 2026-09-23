# V5-B minimal binding learnability v0.1 — C236

## Question and motivation

C235 found low accuracy even on the entire C234 TRAIN set. All12 seed/family/language cells
selected a supplied value100% of the time on TRAIN, but most changed-query pairs kept the same
answer. This is a failure of the fixed training recipe on its training task, not merely an unseen
value-pair generalization miss. See docs/experiment-ledger-addendum-c235-c236.md.

The next question is deliberately smaller: can the unchanged model and optimizer recipe fit a
balanced16-row binding set that requires both factual assignment and queried-object discrimination?
This is a TRAIN-fit probe, not a capability gate for general language or an attempt to relabel C234.

## Minimal cohort

Select existing C234 TRAIN rows with objects [0,1] and sorted values [0,1], preserving original order.
This gives two objects (box/book; 箱/本), values0/1, both assignments, both fact orders, both queried
objects and both languages:2 x2 x2 x2 =16 rows, eight per language.
Examples include `box=0;book=1;box=` -> `0` and `box=0;book=1;book=` -> `1`.
Swapping the assignments changes the required answer for a fixed query; reversing fact order does
not change the object/value relation. A constant answer or always-first/last-value shortcut cannot
pass the paired criterion. A lookup table over all16 seen prompts still could pass: memorization
is not ruled out, and the experiment does not claim it is ruled out.

The original dataset hash and the selected-cohort hash are fixed in the preregistration and code.
Production loads the accepted user-local dataset, calls the actual C234 validator, and selects
rows. The independently reconstructed unit-test fixture is hash-matched to the accepted full
dataset; it is not the production data loader.

## Intervention and fixed elements

Relative to C234, restrict training-cohort breadth from384 to16 rows. Keep both architectures,
13488/10160 parameter counts, width16,48 slots, byte tokenizer, renderer, answer-only objective,
unconstrained256-byte readout, normal/masked views, seeds234001/234002/234003 and final400-step budget.

Fresh Full and common-weight GRU-only models are constructed before either member is trained.
Their initial fingerprints must match the corresponding pre-training fingerprints saved by C234.
No accepted trained checkpoint is used to initialize C236. AdamW, lr0.005, batch32, clip1.0,
betas(0.9,0.999), eps1e-8, weight_decay0 and CPU sampler seed+1000 remain unchanged.
The executable training AST is compared with accepted C234.fit; only the progress label differs.

The endpoint is now performance on the selected16 TRAIN rows, not C234's192-row EVAL endpoint.
It is therefore not a controlled claim that EVAL performance improved. Fewer unique examples,
more repetitions per example, shorter vocabulary coverage and different training-set complexity
are consequences of the cohort restriction, not separately identified effects.

## Measured path

Accepted data -> validated TRAIN16 -> unchanged byte tensor rendering -> fresh model ->400 updates
-> normal/evidence-blind/query-blind TRAIN scoring -> new checkpoint bundle -> reload/replay.
Initial and final evaluation are checked not to mutate weights. All six serialized states are
reloaded with strict schema and identity ordering. Prediction equality, logit/metric replay within
1e-9, final fingerprints and actual forward/row counters are required.

Model forward counters include training and all evaluation/replay calls. Scientific totals:
2400 training forwards plus54 evaluation/replay forwards =2454 model calls.
76800 training row presentations plus864 scoring rows =77664 total row presentations.
Checkpoint writes:one bundle containing all six new states. Test-fixture work is separately scoped
and is not counted as scientific training or scoring.

## Gate and interpretation

For every seed/language cell, use the inherited90% exact accuracy,80% fact-pair accuracy,80%
query-pair accuracy and35-percentage-point evidence/query mask-drop thresholds on TRAIN16.
Each language has8 rows and4 pairs, so the discrete exact/pair thresholds require8/8 and4/4.
Full is the primary family; GRU-only qualification is reported independently.

If all primary cells pass, accept only minimal seen-TRAIN fitting under this recipe. A pass does
not demonstrate held-out binding, useful language, reasoning, memory use, model superiority or
Gate F completion. If a primary criterion misses but execution is valid, accept a valid negative:
the fixed recipe did not solve even this minimal task. That is not architecture-wide impossibility
and does not by itself identify optimizer versus representation versus capacity as the cause.

Any source/artifact/schema/nonfinite/replay/mutation/workload defect is INVALID / RETRY SAME C236.
No threshold relaxation, extra steps, favorable seed replacement, larger model or checkpoint
selection. C235/C234 outcomes remain unchanged. Numeric-memory tuning stays paused.
