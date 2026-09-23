# V5-B saved recombination error audit v0.1 — C243

## Question

When C242 fails new value-pair combinations, does it select the wrong supplied value, produce an
absent value consistent with the fixed TRAIN partner relation, or produce another byte?
Analyze saved final answers only, without changing models, data, checkpoints or the C242 verdict.

C242 passed every TRAIN criterion but all twelve cells missed HOLDOUT. The model's normal TRAIN
accuracy and mask drops do not uniquely establish correct entity binding:TRAIN contains only
pairs0/1 and2/3. The queried value can be inferred from the OTHER entity's value through the fixed
partner map0->1,1->0,2->3,3->2. That rule agrees with all TRAIN targets yet gives an absent value
on each cross-pair HOLDOUT prompt. C243 tests behavioral agreement, not whether the model internally
executes that rule.

## Fixed records and categories

Read the exact C242 split-dataset.json and measurements.json. Keep TRAIN32/HOLDOUT64, row order,
IDs, prompts, targets, languages and all three final prediction views. The writer stores these
predictions after400 updates, and replay_one checks them after reloading each checkpoint.
Do not confuse final[split][language] with initial_train or an earlier final_probe schema.

Recompute every discrete parent metric:normal accuracy, masked accuracies, drops and fact/query/
order pair both-correct scores. Use the identical grouping semantics. Compare within1e-9 to the
saved metrics. NLL is finite/hash-protected only:argmax bytes cannot reconstruct logits or NLL.
The checkpoint file is hashed but never deserialized or executed by the scientific audit.

For each normal answer, use mutually exclusive categories in this order:
correct; other_supplied; absent_partner_of_other; absent_partner_of_queried; other_byte.
For example, in box=0;book=2;box=, the correct byte is0, the other supplied byte2, the training
partner of the other value3, and the training partner of the queried value1. A different byte
remains other_byte; outputs are not constrained or remapped to0..3.

On TRAIN the partner-of-other rule coincides with the correct answer, and partner-of-queried with
the other supplied answer; those rows are classified as correct/other_supplied first. On HOLDOUT
the four digit categories are exhaustive. Therefore merely finding an error in a named category
cannot prove a mechanism. All cell counts and alternative rule agreements must be reported.

## Fixed rules and paired comparisons

Ten normal-view rules:entity,other_entity,partner_of_other,query_fixed_position,first,last,
constant_0,constant_1,constant_2,constant_3. The fixed-position rule maps object0 queries to the
rendered first value and object1 to the second. Partner relations are verified against TRAIN
co-occurrences alone. Rule outputs use factual metadata, not the target field. They are offline
annotations and are never supplied to a model or used to correct its answer.

Retain all fact/query/order pairs, their saved predictions, same-answer flags and both-correct
flags. Fact/query changes require different targets; order changes preserve the target. Each
language has8 pairs of each kind on TRAIN and16 on HOLDOUT. No averaging away seed/language cells.

## Workload and integrity

6 models x(32+64) rows x3 views=1728 unique saved predictions. Normal row records576; ten rules
per row=5760 comparisons; three pair kinds over both splits/languages/models=864 pair records;
24 seed/family/split/language cells. Repeated precheck/postcheck reads are not independent samples.

Scientific model forwards, training steps, checkpoint loads/writes and network calls are zero.
File hashing, JSON work and historical test fixtures still have costs. Five local ignored
artifacts: audit-plan.json,row-errors.json,pair-audit.json,diagnostics.json,validation-summary.json.
Postcheck reloads parent records and recomputes every derived file exactly.

C243 PASS means diagnostic integrity only, independent of which rule matches. Any evidence,
source pin, schema, nonfinite, count or replay fault is INVALID / RETRY SAME C243. Do not relax
C242, invert answers, select a different checkpoint or promote Gate F. A rule match is not a
causal attribution and reused answers are not a new replication. Judge C243 before C244.
