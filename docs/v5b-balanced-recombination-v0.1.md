# V5-B balanced value recombination v0.1 — C242

## Question and motivation

Can fresh models trained with both variable entity values and variable fact positions solve
held-out recombinations of already seen values at the same400-step/batch32 training budget?

C241 had perfect normal TRAIN accuracy, but evidence masking did not reduce it and swapped
assignments scored0%. Its TRAIN_FIT_MISS label is a failure of the full evidence-use criteria,
not a claim that it could not fit normal answers. Fixed TRAIN assignments made factual values
redundant:the query name alone predicted the label. This is an experiment-design limitation.
Do not interpret that outcome as a unique architecture fault or silently rescue C241.

## Dataset

Use the accepted byte-identical C234 dataset, restricted to objects[0,1] (box/book;箱/本).
Values0,1,2,3 already exist in that dataset. Preserve original row order, IDs, prompts and targets.

TRAIN32 uses ordered value assignments:
(0,1),(1,0),(2,3),(3,2).
Each appears with both fact orders, both queries and both languages:4x2x2x2=32.

HOLDOUT64 uses the remaining eight ordered distinct-value assignments:
(0,2),(2,0),(0,3),(3,0),(1,2),(2,1),(1,3),(3,1).
These have the same orders, queries and languages:8x2x2x2=64.

For example, TRAIN includes box=0/book=1 and box=1/book=0, as well as box=2/book=3 and
box=3/book=2. HOLDOUT includes box=0/book=2. Both positions and queries occur throughout.
Every individual value and every entity/value pairing has training support; only the paired
combinations are new. There is no unseen-entity or unseen-token claim.

C242 split SHA256:
9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0.

TRAIN/HOLDOUT prompt, row-ID and assignment-group sets must be disjoint. The original C234 split
field remains source provenance; it does not define the new optimizer membership. C242 models
start fresh and never load checkpoints that were trained on their HOLDOUT rows. This is a new
registered split in an adaptive research series, not a claim of a never-before-examined benchmark.

## Evidence-necessity contract

Before training, audit the joint distribution over language/query/order/target. TRAIN contains
each of32 combinations once; HOLDOUT contains each twice. A query-only or fixed entity-value
lookup can therefore score no more than25% on either split. The particular query-to-fixed-position
rule tested in C240 scores50%. Always-first/always-last also cannot solve all rows.

Group identical evidence-masked prompts and compute the best possible label lookup score:25%.
For identical query-masked prompts the ceiling is50%. These are finite-dataset ambiguity ceilings,
not learned-model measurements or significance tests. No hidden row identity is supplied as input.
The check prevents reintroducing C241's evidence-redundant training distribution.

## Fixed training and measurement

Full13488/GRU-only10160 parameters,width16,48 slots; fresh seeds234001/234002/234003.
Match C241 before-training initial_sha256, not its trained final fingerprint. Copy the common
GRU-only backbone before either paired model is fitted. No parent checkpoint is deserialized.

CPU float64,threads2,deterministic algorithms; AdamW lr0.005,betas(0.9,0.999),eps1e-8,
weight_decay0,clip1,batch32,400 steps/model. Each batch contains all32 TRAIN rows once.
The fit body is AST-matched to C241 except its progress tag; the index helper changes from8x4 to32x1.
Total updates and training presentations are fixed, but training diversity and repetitions change.
This is not a one-variable causal comparison with C241; it is a better-specified learning task.

Only TRAIN is evaluated initially. HOLDOUT is evaluated after step400 and checkpoint replay;
no early stop, favorable seed, best checkpoint or extra training is selected using that score.
Use the actual C234 renderer/evaluator and fact/query paired metrics; both swapped assignments
exist within each split, so fact pairs are valid again. Add order-pair both-correct scoring.

## Gate, cost and limits

Require on both splits, in every primary Full seed/language cell:
accuracy>=0.90, fact/query/order pair both-correct>=0.80, both mask drops>=0.35.
TRAIN has16 rows and8 pairs of each kind per language; HOLDOUT32 rows and16 pairs of each kind.
The integer minima are15/16 answers and7/8 pairs on TRAIN;29/32 answers and13/16 pairs on HOLDOUT.
GRU-only gate is independent. Distinguish TRAIN_CRITERIA_MISS, RECOMBINATION_MISS and BOTH_PASS;
print actual normal accuracy and mask results rather than hiding them behind one label.

Six models x400 =2400 updates/76800 training presentations. Per model:3 initial TRAIN forwards,
6 final TRAIN/HOLDOUT and6 replay forwards. Evaluation rows per model96+288+288=672.
Total2490 full-model forwards/80832 row presentations;one new six-state checkpoint bundle.
New source/artifact protection, exact initial IDs, changed weights, replay and fixed counts are mandatory.

A valid primary miss is ACCEPTED VALID NEGATIVE. An integrity fault is INVALID / RETRY SAME C242.
A pass supports only this bounded recombination task, not general language, core superiority,
causal mechanism identification or Gate F completion. Numeric-memory tuning remains paused.
No paid API, external corpus, model expansion, history rewrite or production runtime modification.
