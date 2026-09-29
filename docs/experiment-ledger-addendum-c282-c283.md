# C282 acceptance and next frozen four-character transfer question

## Formal verdict

C282 ACCEPTED VALID NEGATIVE. The fixed all-five mixed_length criterion was not met:
whole4/5, two_char4/5, triple4/5. The two_char_only control has whole0/5,
two_char4/5, triple0/5. Gate F remains NOT PASSED. Do not rerun C282 or change its gate.

Scientific execution HEAD:aef5aecfc438679641e59b337d7a9eb615c619a3.
Published log commit:b8c0462a27246cf6ff9d9024b614dbca244be2b1.
Publisher log SHA256:4d4c8d0be7f43bf1ecb1f8921a848c5c930c1cad8bb07e3b9363fb3595d427bb.
Publisher log bytes:844576.
Summary:runs/c282-v5b-mixed-length-5ad726e62dfa4eacada5a8cda8c4c27f/summary.json.
Summary SHA256:075cb7399f62d048310bdfb1c31c93ac39ab8b3dc400578d60e062ebfdacf3d1.
Manifest SHA256:291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de.

## Execution validity

Authoritative source/artifact precheck538/950, own32 and focused3949 passed before science.
The log reports run_execution_valid=True, scientific_status=FAIL, candidate_gate=False,
persisted_mixed_length_scores=PASS, protected inputs preserved, clean tracked tree and preserved
execution HEAD. All ten models completed the registered800 updates, both-task evaluation,
checkpoint reload and strict replay. Workload:8000 optimizer updates,384000 training rows,
9080 model forwards,487680 row presentations,36320 core calls,one ten-state bundle write/load
and10 model-state loads. Parent source/test/thresholds were not changed.

## Deciding metrics

|seed|control two-char|control triple|mixed two-char|mixed triple|
|---|---|---|---|---|
|282001|PASS|FAIL|FAIL|FAIL|
|282002|PASS|FAIL|PASS|PASS|
|282003|PASS|FAIL|PASS|PASS|
|282004|PASS|FAIL|PASS|PASS|
|282005|FAIL|FAIL|PASS|PASS|

The intervention raises complete three-character and whole-state pass counts from0/5 to4/5,
while the original two-character count remains4/5 with a different failing seed.
For mixed seed282001, all reported triple TRAIN normal totals are96/96, while its six triple
HOLDOUT totals are40,40,40,38,45,44 out of48. Its reported two-character HOLDOUT totals are
39,40,39,37,44,43 out of48. This suggests a held-out-value-combination failure rather than
inability to fit the reported triple TRAIN prompts; no unreported criterion cause is inferred.
Do not call four successes a five-seed reliability PASS.

## Interpretation and limits

The fixed-budget coverage change is useful in this cohort: multiple final states can satisfy the
complete two/three-character binding criteria without more parameters or optimizer updates.
It does not establish universal optimization reliability, unseen-length transfer or a variable-length
algorithm. mixed_length trained on three-character TRAIN renderings. Its successful HOLDOUT rows
hold out value combinations, not identifier length.

The user's hypothesis that covering multiple lengths improves success on a completely unseen length
is now testable with the existing checkpoints. Perfect C282 reliability is not a prerequisite to
measure that transfer, provided every seed is retained and the known C282 miss remains unchanged.

## Accepted artifacts (SHA256; bytes)

- architecture-plan.json:291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de;3281.
- dataset.json:1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;36024.
- triple-dataset.json:432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;158236.
- trained-models.pt:8cadcfb73017fad6f82d86ba37a365cdf40ce3adcb304a531b34533300164cce;1238007.
- evaluations.pt:b0816dc5a82a200f5e2537321df491e1802fd01177b55ffbc46cf0daf08d4267;106287783.
- measurements.json:a92b92881f0ffc7c7b6a6286c7e0237d469e35f5d532269b48a34d0ee96255fd;524693.
- validation-summary.json:27d4db76f97b24941e3c88dc95a9453fe51e1521a340447d0bbe44c609369af7;19584.

## Next question, not activation

Do the frozen C282 mixed_length states transfer better to four-character identifiers than their
matched two_char_only states, with no further training and no seed selection?

Plan a separate C283 frozen evaluation of all10 states, seeds282001..282005. Retain the architecture,
48-token bound and fixed thresholds. Four-character repeated/shared-prefix3/shared-suffix3 profiles
must be new to both training arms, preserve logical facts/queries/value splits, and fit English and
Japanese without truncation. Replay the original two/three-character outputs before and after the
new evaluation. Do not change model configuration to accommodate evaluation.

Report four-character fixed-gate pass counts, paired correct/collapse contrasts, per-seed and
per-language/profile behavior. Candidate gate may concern all5 four-character states only; passing
it never repairs the already-failed C282 both-task gate or promotes Gate F. Comparisons retain the
failed mixed seed282001 and failed control seed282005.

This contrast combines length diversity, larger maximum training length, and per-length exposure
allocation. Even positive transfer cannot isolate diversity alone versus proximity to the four-character
test; that would need a later three-character-only control. No extra training/control is added now.
Four-character transfer is bounded evidence, not arbitrary-name or arbitrary-length generalization.

C283 requires its own preregistration, sealed manifest, implementation, behavioral tests and committed-
byte post-authoring review before activation. C284 NOT REGISTERED.
