# V5-B complete-cohort sampler v0.1 — C238

## One question

With C236's16 TRAIN rows, model architectures, fresh initial weights, optimizer and400-step budget
fixed, does replacing random replacement batches with the complete16-row cohort repeated twice
permit the minimal TRAIN probe to be fitted?

C237 observed numerical input/encoder/readout/logit responses without correct answer switching.
It did NOT identify sampling as the cause. This is a controlled sampler hypothesis, not an inference
that the fault has already been located. See docs/experiment-ledger-addendum-c237-c238.md.

## Intervention

C236: each update samples32 row indices with replacement from16 rows.
C238: each update uses [0,1,...,15,0,1,...,15] in the existing row order.

Every row appears exactly twice per batch and800 times per model over400 updates. Each batch
contains16 targets0 and16 targets1, and balanced language/query/order/assignment combinations.
There are still32 presentations per update; batch size and total presentation budget do not grow.
The average cross-entropy, optimizer settings, clipping and update count remain unchanged.

This simultaneously changes complete-cohort coverage, batch label balance and stochastic-gradient
variability. Even a positive result cannot isolate label balance alone. Existing data/model facts
and the sample membership, rather than a new target-derived input, determine the fixed index list.

## Paired comparator and initialization

Reuse the accepted C236 measurements as the random-sampler comparator. Do not rerun C236 or train
another baseline secretly. Its negative result remains fixed. For all three seeds and both model
families, initialize new models from the same seed; match C236's initial_sha256 and initial_probe
before any C238 update. Never continue from C236's final trained state or C237's captured state.
Construct the common-weight GRU-only copy before either paired model is trained.

The exact C234 evaluator, normal/evidence-blind/query-blind views,16 rows, target bytes and256-way
unrestricted byte output remain unchanged. Full13488 parameters and GRU-only10160; width16/48 slots.
AdamW lr0.005, betas(0.9,0.999), eps1e-8, weight_decay0, clipping1.0, batch32,400 steps/model;
CPU float64, two threads, deterministic algorithms. No architecture, data, loss or runtime change.

An AST comparison transforms precisely the C236 ids assignment into
`balanced_indices(len(train_targets))`, permits only the C236/C238 progress-tag difference, and
requires the rest of fit to match. Training constants must also match. The original CPU generator
construction is intentionally retained but not consumed; it does not choose C238 indices.

## Gate and scope

Reuse the exact C236 metric implementation and thresholds: every primary Full seed/language cell
must have exact accuracy>=0.90, fact-pair>=0.80, query-pair>=0.80 and both mask drops>=0.35.
At8 rows and4 pairs per language, the exact/pair thresholds require8/8 and4/4. GRU-only qualification
is reported separately; it cannot turn a Full miss into a primary PASS. Print each candidate
accuracy beside its fixed C236 accuracy and their descriptive difference.

A valid Full miss is ACCEPTED VALID NEGATIVE. A Full pass supports only fitting these16 seen
prompts under complete-cohort sampling; memorization is possible. No held-out-language claim,
core-superiority claim, C236 rescue or Gate F completion. No more steps, favorable seed selection,
learning-rate adjustment, early stopping or best-checkpoint choice after seeing a result.

## Integrity and cost

Six new models x400 updates =2400 training steps /76800 answer presentations.
Initial/final/reloaded evaluation:54 model forwards /864 row presentations.
Total2454 model forwards /77664 row presentations. One checkpoint bundle with six states.
No comparator forward or training; no held-out evaluation or scientific network call.

Actual model hooks count calls and rows. Initial fingerprints and metrics must match the recorded
C236 before-training state. Evaluation must not mutate weights. Final trained states must change,
be saved/reloaded in the registered identity order, and replay predictions exactly and logits/
metrics within1e-9. The result retains the accepted C236 final metrics without modifying them.

Postcheck verifies all input/output hashes, plan and cohort identity, summary recomputation and
recorded comparator/initial metrics. Invalid identity, schema, source protection, nonfinite values,
replay, counts or test failure stops same C238. Transport failure alone does not justify retraining.
Gate F remains NOT PASSED; numeric-memory tuning stays paused.
