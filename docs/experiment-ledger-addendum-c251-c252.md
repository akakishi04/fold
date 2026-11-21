# C251 acceptance and C252 query-source boundary

## Formal verdict

**C251 ACCEPTED VALID NEGATIVE.** Gate E PASSED; Gate F NOT PASSED.

Scientific execution HEAD: `9fb7e7cfec2521815258cf2f0c3b433bcea6419d`.
Published log commit: `36555face557650c73521ef0709063ba4ae7f8c7`.
Publisher log SHA256: `0cf296dca8d7633cd3b4d8547a5b2be408d21675a961355743006ee01a25e694`.
Log bytes: 620744.
Summary SHA256: `55038562223ac2bf87db09d2f102d9bd0ca6aacaeaf1381186a836330e26578c`.
Local summary: `runs/c251-v5b-precore-read-dcc6ca85fe504ea7a71db741ab1558b1/summary.json`.

24 own tests PASS in27.509s;3193 focused tests PASS in194.369s.
352 source pins/563 protected inputs. Five models completed400 updates each:
2000 updates/64000 training presentations;2075 full-model forwards/67840 row presentations.
All initial/checkpoint/prediction replays,weight updates,protected inputs,tracked tree and execution
HEAD checks passed; `run_execution_valid=True`. Scientific status FAIL;candidate_gate=False.

## Deciding metrics

Every candidate TRAIN language cell passes the registered criteria. HOLDOUT normal correct counts
(each language /16), with immutable C250 Full/token_read comparator in parentheses:

| Seed | EN | JA | Whole-seed candidate | Whole-seed C250 |
|---:|---:|---:|---|---|
|250001|16 (3)|16 (8)|PASS|MISS|
|250002|10 (6)|9 (8)|MISS|MISS|
|250003|10 (16)|10 (16)|MISS|PASS|
|250004|6 (2)|5 (2)|MISS|MISS|
|250005|16 (16)|16 (16)|PASS|PASS|

Candidate outcomes:BOTH_PASS4 language cells,RECOMBINATION_MISS6.
Whole-seed both-language passes:2/5,identical in count to C250 but not identity:
C251 passes250001/250005;C250 passes250003/250005.
Descriptive pooled HOLDOUT correct:114/160 candidate versus93/160 comparator.
Ten paired language deltas:6 improve,2 tie,2 worsen. These are correlated cells from the same five
initializations and reused task;no significance or population-reliability claim.

## Interpretation and non-claims

Changing only Full reader memory from post-core token states to pre-core local-encoder states did
not improve whole-seed reliability under the fixed all-seed gate. It materially changed the
optimization outcome:one previously failing seed became perfect while one previously perfect seed
fell to10/16 in both languages. Thus memory source matters to the learned solution,but simple
pre-core substitution is not a stable remedy.

Do not conclude that the core destroys information,that pre-core memory is better in general,or
that C250/C251 are statistically equivalent. The intervention changes both forward representation
and gradient paths. The adaptive HOLDOUT has been repeatedly inspected and is not an external
confirmation set. C248/C250 verdicts remain unchanged;no production adoption or Gate F promotion.

## Accepted artifacts

- measurements.json: `c98c5e6bbe313eac35895290d06f002756816918d7341de946941ab70ed0c398`
- precore-plan.json: `2f72dec74e0fe27e9a9aba129dd1064b34a467363b5a8dc9f5a7a3a2c636fc87`
- split-dataset.json: `e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346`
- trained-models.pt: `0fce9c6e666360cf28a3723f870565a7aa1308bfa2a9a524c9a804080dc1e5c1`
- validation-summary.json: `f4b5128aeb4d730a4227a2c820cdc21874ae269c3ea3c3f669d0202390227da2`

## Next question, not registration

Hold the C251 pre-core K/V memory and post-core residual state fixed. Change only the attention
query source from post-core EOS to the corresponding pre-core local-encoder EOS representation.
Does representation-space alignment improve the same five-seed Full result?

The candidate should retain the exact C251/C250 initial state,parameters,training data,schedule and
budget. The FOLD core must still execute and train;the output residual base remains the actual
post-core EOS state. Only q=Wq*h_query changes its h_query source. Compare against immutable C251
endpoints on all five seeds. This is an adaptive matched comparison,not a retry or seed rescue.
A valid miss remains negative;an integrity fault retries C252 only.
