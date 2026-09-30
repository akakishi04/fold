# C289 acceptance and next saved pair-margin audit

## Formal verdict

C289 ACCEPTED VALID NEGATIVE. Candidate pair_early passed 0/5 four-character gates,
versus ce_only 3/5 and pair_always 0/5. C289 is complete; no rerun is authorized.
Gate F remains NOT PASSED. C288 and all earlier verdicts remain unchanged.

Scientific execution HEAD:b5026f48e0c8b39bbfb9069f34271d7b6ba9d50f.
Published log commit:b96ab8b01ec9c9eb876fada8339c8c0e0d0a8e12.
The publication commit adds only docs/experiment-run-logs/c289/latest.log and latest.json.
Log Git blob:08e44c7220bcf74a710931ca82028edbfe462b29.
Metadata log SHA256:44d17b9b49fb49645d1dd6181d95cd998c4ce501238988de0450f6bf81bf7045.
Metadata log bytes:1121539.
Summary:runs/c289-v5b-early-pair-ac332442137243e68d4ec3bd754ba717/summary.json.
Summary SHA256:151117fcd43177b8e393eeee6935222e54f01caecf8a17b4656149aec5058897.
Manifest SHA256:48b33a7ed29cf9ded858753d5f64210006f559ef428c167e912621a71896ae21.

## Execution validity

Published log shows own48 and focused4205 completed,authoring_runtime_preflight=PASS,
all_auxiliary_prefixes_matched=True,persisted_early_pair_scores=PASS,tracked_tree clean,
execution_HEAD preserved,and final run_execution_valid=True. scientific_status=FAIL;
candidate_gate=False. The exact shared400-update prefix requirement was not waived.
Registered workload:15 models,12000 updates,576000 training rows,14430 forwards,
809280 total row presentations,57720 core calls,one final bundle write/load and15 strict loads.
The child verifier must reconstruct the accepted eight artifacts through the exact frozen summary
hash and C289.verify_artifacts;do not replace their hashes or infer them from a prior experiment.
The evaluator schema is fold-c289-early-pair-eval-v1;checkpoint schema is
fold-c289-early-pair-models-v1. No author-side re-execution of user-local science is claimed.

## Deciding metrics

|gate|ce_only|pair_always|pair_early|
|---|---:|---:|---:|
|quad primary|3/5|0/5|0/5|
|two_char full|3/5|4/5|4/5|
|triple full|3/5|4/5|4/5|
|all tasks|3/5|0/5|0/5|
|fitted TRAIN direct|4/5|5/5|4/5|
|seen-length HOLDOUT direct|3/5|4/5|4/5|

-289001:all arms fail full tasks/HOLDOUT;ce_only and pair_always pass trained-length
 TRAIN direct criteria,but pair_early fails those criteria.
-289002:CE fails all full tasks and trained-length TRAIN direct;both auxiliary arms
 pass two/three and their TRAIN/HOLDOUT direct criteria,but fail quad.
-289003/289004/289005:CE passes every task;both auxiliary arms pass two/three but fail quad.
All15 states and all5 seeds are retained.

The all-five gate miss does not mean every four-character answer is wrong. For289002,
both auxiliary arms score576/576 on quad inherited TRAIN values and287/288 on HOLDOUT;
the HOLDOUT miss fails one accuracy and query-pair cell. For289005,both auxiliary arms
score572/576 and284/288,with4/1 collapsed pairs. This illustrates why pooled answer quality
and all-local-criteria reliability must be reported separately.
For289001,early withdrawal loses trained-length fitting:two/TRAIN569/576 and
triple/TRAIN570/576,versus576/576 each with always-on supervision.

## Interpretation and non-claims

The fixed early-withdrawal policy did not rescue any quad seed relative to always-on,
and it did not preserve all of always-on's TRAIN direct passes. The supervised-pair approaches
helped seen-length task gates on289002 while losing all three CE-only quad-success seeds.
Neither always-on nor this early schedule is adopted as a general solution.

Do not claim that stopping at another update or changing the coefficient will work.
Equal gate counts do not imply identical individual predictions or logits. Low pair-assignment
loss does not logically guarantee both answers correct;that known limitation needs measurement
on the actual retained outputs before changing the objective again. C289 does not identify a
unique optimizer,architecture,margin-saturation,or late-pressure cause. Across-C288/C289 rate
changes are not one-factor comparisons because their seed cohorts differ.

## Next question, not activation

For every retained C289 normal-output query pair,how often does the auxiliary assignment
margin meet its registered margin while one or both individual answers remain wrong,
and does early withdrawal change the same individual predictions versus its two anchors?

C290 should be a zero-neural saved-output diagnostic,not another weight/switch sweep. Preserve
all arms,seeds,tasks,TRAIN/HOLDOUT splits and original gates. Compute the existing pair margin
and pair penalty from saved logits;cross-tab against independent answer correctness/collapse,
then compare aligned early/always and early/CE predictions. A diagnostic PASS certifies exact
reconstruction only. Existing gate thresholds and verdicts must not change.
C290 requires separate implementation,preregistration,committed-byte review and runtime Validate.
C291 NOT REGISTERED.

## Evidence transport note

This log exceeds1MiB. GitHub Contents reads may return empty text even with line ranges.
The immutable Git blob was fetched instead,and small line ranges of the returned resource were
used for counts and the final POSTCHECK. Never infer PASS from publication or an empty Contents
response. Avoid expanding the single huge RESULT JSON line when reading the resource.
