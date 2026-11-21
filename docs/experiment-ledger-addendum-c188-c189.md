# C188 acceptance / C189 handoff

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

## Formal judgment

**C188 — ACCEPTED PASS.**
**C189 NOT REGISTERED at this acceptance commit.**
Gate E remains **NOT PASSED**. All earlier judgments, checkpoints, preregistrations and
valid negatives remain unchanged.

Successful C188 execution identity:
- execution HEAD: `683d795b12d4f0aada4850dcac2a010e699882ad`
- run: `runs/c188-v5e-multimissing-target-selection-81830a0e8ba741519c9172bdf2f7a7bc/summary.json`
- summary SHA256: `2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153`
- focused regression: **1413/1413**, 43.155s
- source/artifact precheck: PASS
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- `run_execution_valid = True`
- production runtime modified: **False**
- Gate E candidate: **False**

Uploaded C188 log:
- bytes: 315279
- SHA256: `8f8308404031fc894db07360f80b54eebff3c64db05fc84e7eb50fba5dc1887b`
- canonical reconstructed summary: 79138 bytes
- reconstructed summary SHA256 matches the run exactly.

## Deciding evidence

C188 froze the three accepted C181 INTERNAL_SEMANTICS bases (181001/181002/181003)
and crossed them with fresh target-head seeds 188001/188002/188003.

Primary discriminating PILOT cohort:
- 528 NEEDS rows total
- missing2: 376 rows
- missing3: 152 rows

Formal TRAIN-only syntax-blind frequency reference:
- missing2: 268/376 = 0.7127659574468085
- missing3: 128/152 = 0.8421052631578947
- equal m2/m3 macro = 0.7774356103023516

Every one of the nine frozen-base/head combinations achieved:
- missing2: **376/376 = 1.0**
- missing3: **152/152 = 1.0**
- macro: **1.0**
- selected observed facts: **0**

The strict per-combination gate therefore passes 9/9 with no averaging or best-head
rescue.

Secondary full multi-missing PILOT cohort:
- 1768 rows
- missing2: 1152/1152
- missing3: 616/616
- every selector: **1768/1768 = 1.0**

All three same-head-seed copies also preserved preregistered paired construction:
for each head seed, initial target-head fingerprint is identical across all three frozen
bases and minibatch schedule hash is identical across all three frozen bases.

Workload:
- frozen base loads: 3
- trained target heads: 9
- target updates: 18000
- sampled TRAIN rows: 4608000
- frozen base feature rows: 16776
- frozen base forwards/cell calls: 18/126
- PILOT selector predictions: 15912
- actual acquisitions/network/evidence writes/answers/proofs: 0

## Scientific interpretation

C188 establishes, only in the registered C174 development family, that a small learned
selector can use frozen accepted C181 internal graph states to choose a currently
influential missing fact among multiple unobserved facts, and can do so substantially
better than the registered TRAIN-only syntax-blind frequency reference.

The selector is not merely exploiting a low-index convention:
FIRST_UNKNOWN scored only 0.5263157894736843 macro, while the formal frequency reference
scored 0.7774356103023516 and all nine learned selectors scored 1.0.

The result is stronger than the minimum C188 claim because all nine selectors also scored
the entire 1768-row multi-missing NEEDS secondary cohort perfectly.

## Claim / non-claim

Claim:
- frozen C181 internal states contain target-selection signal sufficient for the registered
  selector to choose an influential unknown fact on this development family;
- the result is stable across all three accepted base seeds and all three fresh head seeds;
- observed facts are never selected.

Non-claim:
- no live acquisition is driven by the learned target in C188;
- no learned tool/provider choice, retry or stopping;
- no claim that the selected fact is globally optimal information gain;
- no repeated-variable, larger-expression, natural-language or independent final holdout;
- no answer/proof generation;
- no Gate E completion or production adoption.

The four PILOT semantic groups are repeatedly inspected development groups. The target
teacher is programmed logical supervision. A 1.0 score here is therefore bounded evidence,
not a final generalization claim.

## Reviewer verification boundary

The uploaded C188 log was parsed as a complete RESULT payload. The canonical reconstructed
summary is 79138 bytes and hashes exactly to the reported summary SHA256 above.

Independently rechecked from the uploaded summary:
- exact 9 selector identities/order;
- all nine strict per-selector gate comparisons;
- all primary 528/528 target hits;
- all secondary 1768/1768 target hits;
- selected-observed count zero;
- paired initial-head fingerprints and minibatch schedules by head seed;
- workload counts and parent identity.

Separate C188 artifacts, target-head checkpoint bytes, the NPZ contents and the user's
1413 regression tests were not independently rerun by the reviewer.

## Next single boundary

The next proposed question is live integration:

> Can the accepted frozen C181 necessity model and one frozen C188 target selector,
> sharing the same initial forward, drive exactly one real C172/C173 RETRIEVE of the
> learned selected fact in multi-missing cases and then reclassify the actual updated
> state correctly?

Keep C189 bounded:
- no new training;
- original canonical C174 local fact layout only, so live target integration is not
  confounded with another renaming experiment;
- exactly one real acquisition attempt per episode;
- both possible selected-fact bit values;
- no answer/proof generation and no second acquisition even if the post state still NEEDS.

C189 must be separately preregistered after this acceptance commit.
