# V5-B two-partner recombination v0.1 — C244

## One question

Can the unchanged fresh models generalize to held-out pairs when each TRAIN value has two possible
partners rather than one, at the same 400 updates, batch32 and total training presentations?

C243 found 215/384 HOLDOUT answers absent from the prompt, including 166 matching the TRAIN
partner of the nonqueried value. This is not a unique mechanism diagnosis. However, C242's
one-partner training distribution admitted a perfect nonqueried-value lookup. C244 removes that
specific identifiability problem over the TRAIN union without claiming to remove every shortcut.

## Fixed data partition

Reuse all existing box/book, four-digit rows from C242's TRAIN32/HOLDOUT64 artifacts. Preserve
row bytes, labels, provenance, both fact orders, both queries and both languages.

Old balanced block32: (0,1),(1,0),(2,3),(3,2), exactly C242 TRAIN in its saved order.
Added balanced block32: (0,2),(2,0),(1,3),(3,1), filtered from C242 HOLDOUT preserving saved order.
C244 TRAIN64 is old block followed by added block.
C244 HOLDOUT32: (0,3),(3,0),(1,2),(2,1), filtered from C242 HOLDOUT in saved order.

Every ordered assignment contributes 2 orders x 2 queries x 2 languages = 8 rows.
Each individual block contains all language/query/order/target combinations once.
Every value has two distinct TRAIN partners; exact prompt, row-ID and assignment-group sets are
TRAIN/HOLDOUT-disjoint. Original split labels remain source provenance, not current membership.
All individual values/entity-value combinations have TRAIN support. No unseen-word claim.

For example, TRAIN now includes box=0/book=1 AND box=0/book=2, with reversed assignments as well.
Learning only 'the other value 0 means answer 1' cannot solve the entire new TRAIN set.

On the complete TRAIN union, a function given language/query/order/nonqueried value can score
at most 50%, instead of C242's 100%. Query-only lookup is bounded by25%; identical evidence-masked
inputs by25% and identical query-masked inputs by50%. These are exact finite-dataset ambiguity
ceilings, not statistical chance levels. They are checked before learning. A block in isolation
still has a unique partner map; only the full union breaks it. No block/step identifier is input.

## Fixed learning budget and disclosed changes

Construct fresh Full13488/GRU-only10160 models from seeds234001/234002/234003. Match C242's
initial_sha256 before learning; do not load a trained C242/C243 checkpoint. Create the common-weight
GRU-only comparator before either paired model trains. Width16,48 slots, byte renderer and
unrestricted256-byte output remain unchanged.

AdamW lr0.005, betas(0.9,0.999), eps1e-8, weight_decay0, clip1, batch32,400 steps, CPU float64,
threads2, deterministic algorithms. Alternate full balanced blocks: update1 old, update2 added,
through update400 added. Exactly200 updates per block and200 presentations per TRAIN row.
The exact model input batch is checked on every training forward, not only inferred from counters.

C242 saw32 rows400 times; C244 sees64 rows200 times. Training presentations stay76800 across six
models. Dataset coverage, repetitions and update schedule change jointly. Last-block effects,
inter-block interference or other optimizer behavior remain possible; do not attribute a difference
uniquely to partner ambiguity. Do not reverse the schedule after seeing an unfavorable result.

The fit body equals C242 except the experiment tag and step-dependent index expression. Initial
evaluation is TRAIN only. Final TRAIN/HOLDOUT is at step400 and after reload. HOLDOUT cannot
control optimizer steps, early stopping, selection, hyperparameters or a second run.

## Scoring and comparison

Reuse C242's evaluator and validators, which accept row counts dynamically, and its underlying
C234 fact/query metric implementation. Both directions and orders exist, so all fact/query/order
pairs are valid. TRAIN has32 rows/language and16 pairs/kind; HOLDOUT16 rows and8 pairs/kind.

Full primary gate: every seed/language meets BOTH split criteria:
accuracy>=0.90; each fact/query/order pair score>=0.80; evidence/query mask drops>=0.35.
Integer minima TRAIN29/32 correct and13/16 pairs; HOLDOUT15/16 and7/8 pairs.
GRU-only is independent. A valid miss is ACCEPTED VALID NEGATIVE, not an execution fault.
A pass is bounded held-pair transfer only, not general language or core superiority.

C242's full HOLDOUT64 is not the same evaluation set. Recompute all its discrete metrics from
saved answers on precisely C244's remaining HOLDOUT32, using row-ID correspondence and all three
views. Store those beside C244 results; compare like with like. This comparator is descriptive,
not a fresh retraining or independent sample. No NLL reconstruction from answer bytes.
Promoted training rows must never enter the common-HOLDOUT comparator. Selection was fixed from
pair identities, not row-level score selection. This is an adaptive internal development series,
not an untouched external benchmark.

## Integrity, workload and stop

Six models x400=2400 updates/76800 training presentations. Per model:3 initial TRAIN forwards/192
rows,6 final forwards/288 rows and6 replay forwards/288 rows. Total90 scoring forwards/4608 rows;
2490 model forwards/81408 total rows. Before reload409 forwards/13280 rows; after415/13568.
One new six-state checkpoint bundle. No parent model inference or scientific network calls.

Require exact initial/final identities, changed weights, non-mutating evaluations, actual batch
membership/block counts, strict checkpoint schema/order, exact prediction replay and logit/metric
error<=1e-9. Postcheck verifies artifacts, partition, initial identity, common comparator and child
discrete metrics. Any integrity fault is INVALID / RETRY SAME C244.

Gate F remains NOT PASSED. Preserve C242/C243 verdicts and all source/test/log evidence. No model
expansion, more training presentations, paid API, external corpus, cleanup, history rewrite or
production runtime change. Numeric-memory tuning remains paused. Judge C244 before C245.
