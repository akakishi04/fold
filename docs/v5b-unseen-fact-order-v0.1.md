# V5-B unseen fact-order transfer v0.1 — C257

## One question

Can the ten frozen final C256 models answer the same three-entity assignments when the facts are
presented in the four orders never used for C256 training or evaluation?
This is a capability evaluation without additional training, not an internal-activation diagnostic.

C256 used only abc and cba (or 甲乙丙 and 丙乙甲). Entity b/乙 therefore always occupied the middle
fact position. Its value-assignment PASS does not establish arbitrary order transfer.
C257 adds acb, bac, bca and cab while retaining every entity-value pair and the queried entity.

Example: a=0;b=1;c=2;b= and c=2;a=0;b=1;b= both have target 1.
No prompt is sorted back into a trained order before inference. The renderer must actually present
the new order. No target, permutation index or entity ID enters the model outside the visible bytes.

## Fixed models and data boundary

Strictly load all ten accepted C256 final states: five seeds256001..256005, paired aligned_precore_read
and eos_adapter arms. Use the existing C256 factory/make_model and the actual C252/C248 classes.
All models remain eval with requires_grad=False; parameters and all accepted sources are protected.
There is no optimizer, new initialization study, fine-tuning, seed replacement or checkpoint selection.
Freshly constructed wrappers only receive the saved final state before any evaluation.

Original C256 dataset: TRAIN144/HOLDOUT144 rows, two orders, two languages, three queries per assignment.
The labels TRAIN/HOLDOUT refer only to the original C256 assignment split; C257 performs no training.
New data: TRAIN288/HOLDOUT288 rows, four new orders with those same assignments/languages/queries.
Each new row retains its original canonical row ID as provenance. Exact assignment sets remain
separated between TRAIN and HOLDOUT. No old or new prompt is silently truncated or rewritten.

## Measurement sequence

For each frozen model:
1. Score all original C256 rows/views through actual C256.evaluate. Match saved predictions exactly
   and all saved metrics including NLL within1e-9 before presenting any new order.
2. Score the four novel orders in two batches per view, one per assignment split.
3. Score the original rows/views again and require raw-logit restoration within1e-9 and exact argmax.
4. Verify unchanged final-state fingerprints and the exact forward/row count.

New-order output tensors must be finite CPU float64. Threads2 and deterministic algorithms remain.
Raw logits from all three stages are stored, allowing postcheck to reconstruct every score without
further model evaluations. C256 did not save its raw endpoint logits; initial anchor replay therefore
compares its saved metrics/predictions, not nonexistent prior logit arrays. The restoration comparison
uses the freshly recorded original anchor logits from the same C257 run.

## Fixed capability gate

Require every candidate seed to satisfy all of the following for both languages and both assignment
splits. EOS controls are reported independently and cannot rescue or fail the candidate gate.

- Original C256 cell criteria remain satisfied.
- Every novel permutation separately: accuracy>=0.90, query-triplet accuracy>=0.80,
  evidence-mask drop>=0.35 and query-mask drop>=0.35.
- All-six-order consistency>=0.80: for each assignment/query, all six presentations must be correct.

Each new order/language/split cell has36 questions and12 three-query groups, requiring at least33/36
answers and10/12 triplets. Six-order consistency has36 groups per language/split, requiring29/36
fully correct groups. A weak order cannot be hidden by averaging it with the other three.

Report every permutation separately, both original assignment splits, both languages and all ten
models. Report whole-seed passes for each arm and reasons ORIGINAL_CRITERIA_MISS, NEW_ORDER_MISS,
SIX_ORDER_MISS or PASS. Original criterion misses are expected for some EOS controls; original
replay mismatches are execution faults, not control performance outcomes.

## Workload and scope

Per model: original6 forwards/864 rows; new6/1728; restoration6/864.
Total10 models:180 full-model forwards/34560 row presentations.
Training0, checkpoint bundle loads1, strict final-state loads10, new learned checkpoint writes0.
Saved logits are evaluation artifacts, not new learned weights. Historical test computations,
parent-file hashing and serialization are separate work and are not independent science samples.

PASS establishes only frozen order transfer within this finite authored assignment family.
It does not establish arbitrary-length reasoning, unseen vocabulary, ordinary English/Japanese
proficiency, core superiority, production readiness or Gate F. Failure does not revoke C256's
value-assignment PASS. No inference correction or learning is introduced after inspecting scores.

Judge C257 before registering C258. Preserve all prior results and the C256 recovery record.
