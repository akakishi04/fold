# V5-B fact-order holdout v0.1 — C239

## Question

C238 fitted all16 seen prompts using complete-cohort batches. Does this recipe transfer to an
unseen ordering of the same facts when that order is excluded from the new model's training?
This removes the exact-prompt resubstitution limitation. It does not test new facts, values or nouns.

## Partition and fresh initialization

Reuse the byte-identical16-row C238 pool. Select order0 as TRAIN8 and order1 as HOLDOUT8, retaining
original row order and bytes. Both partitions contain both value assignments, both queried objects
and English/Japanese. Each language has4 rows and2 fact/query pairs in each partition.

Example TRAIN: `box=0;book=1;box=` ->0, `box=0;book=1;book=` ->1.
Example HOLDOUT: `book=1;box=0;box=` ->0, `book=1;box=0;book=` ->1.
The other assignment swaps0/1. Japanese uses the same existing box/book names and rendering.

Exact prompts and row IDs are disjoint. Fact-group IDs intentionally overlap because the tested
change is presentation order. This is not a group-disjoint fact or entity/value benchmark.
Parent rows retain their original split="TRAIN" provenance. The new outer TRAIN/HOLDOUT partition,
not that inherited metadata field, determines C239 optimizer membership. Do not silently relabel
or mutate accepted parent data to disguise this distinction.

Never initialize from C238 trained checkpoints: they have seen both orders. Construct fresh models
with the same three seeds and match the C238 initial_sha256 values before any learning. Make the
independent common-weight GRU-only copy before either paired model trains. Initial metrics now
refer only to TRAIN8, so do not require equality with C238's all16 initial metrics.

## Training and evaluation

Retain architectures, parameters13488/10160, width16/48 slots, byte renderer and256-class output,
AdamW lr0.005, betas(0.9,0.999), eps1e-8, weight_decay0, clip1, batch32 and400 steps per model.
CPU float64, threads2, deterministic algorithms. Each update contains all8 TRAIN rows4 times.
The fit body is AST-identical to C238 apart from its progress label; the complete-cohort index
helper now repeats8 rows4 times rather than16 rows2 times. No other training change is allowed.

Only TRAIN is scored before training. Fit takes TRAIN tensors and targets, not a combined dataset
or a held-out argument. HOLDOUT tensors are first rendered for model evaluation after step400.
No early stopping, hyperparameter/seed choice, best-checkpoint selection or continued learning.
Each retained row receives1600 presentations/model, rather than C238's800: this follows from the
restricted cohort at fixed update/batch budget and is not an independently isolated variable.

The actual C234 renderer/evaluator/paired-metric implementation is reused. C236/C238 validators
that hard-code8 rows per language must not be used on the new4-row metrics. C239 has its own
explicit split/count validator and final TRAIN/HOLDOUT record schema.

## Counts and gate

Six models x400 steps =2400 updates and76800 training presentations.
Per model: initial TRAIN3 + final TRAIN3/HOLDOUT3 + reloaded TRAIN3/HOLDOUT3 =15 evaluation forwards.
Total90 evaluation forwards over8 rows =720 evaluation presentations.
Scientific totals2490 model forwards /77520 row presentations. One new six-state checkpoint bundle.
No scientific network calls, no parent-checkpoint forwards, and no automatic follow-on experiment.

Retain numerical thresholds: exact accuracy>=0.90, fact/query paired accuracy>=0.80,
evidence/query mask drops>=0.35. With4 rows and2 pairs per language, exact and paired thresholds
require4/4 and2/2. Require every Full seed/language cell to pass on BOTH TRAIN and HOLDOUT.
Report the GRU-only gate separately. A baseline pass does not substitute for Full.

Report TRAIN_FIT_MISS when TRAIN criteria fail, ORDER_HOLDOUT_MISS when TRAIN passes but HOLDOUT
fails, and BOTH_PASS when both pass. These localize outcomes; they do not identify internal causes.
A primary miss with valid execution is ACCEPTED VALID NEGATIVE. An integrity fault is INVALID /
RETRY SAME C239. A pass supports only this fixed one-direction fact-order transfer. It does not
establish general language, new-value/entity generalization, memory competence or core superiority.

## Integrity and stop

Pin and hash inherited sources and artifacts, plus the C238 summary/artifacts and OWN6 additions.
Verify fresh initial fingerprints, changed trained weights, non-mutating evaluation, actual forward
counts and presented rows. Reload all six states in fixed identity order, reproduce exact argmax
outputs and logits/metrics within1e-9 on both partitions. Verify saved split, plan, measurements,
summary and artifact hashes/sizes. Preserve all prior verdicts and evidence.

No larger model, external corpus, paid API, history rewrite, cleanup or production runtime change.
Gate F remains NOT PASSED; numeric-memory tuning stays paused. Judge C239 before registering C240.
