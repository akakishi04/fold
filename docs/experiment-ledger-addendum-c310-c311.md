# C310 formal acceptance — saved-value diagnostic

C310 ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY). C309 remains ACCEPTED VALID NEGATIVE.
C308 remains ACCEPTED PASS within its original bounded task. Gate F NOT PASSED.
C311 NOT REGISTERED at the acceptance commit. C310 is not a new capability gate.

## Evidence identity
Scientific execution HEAD: bdbf7c4c410ceb9d621ae5d3ecf86e764061550b.
Published log commit: 45da9b7b1f63375bf0af251a7f65cc0c83b76765.
Metadata: docs/experiment-run-logs/c310/latest.json.
Console: docs/experiment-run-logs/c310/latest.log.
Log SHA256: 2acfb310a6716eada4185c7a3462a652ae8168a23e1a15d443b14718fe605c5b.
Summary: runs/c310-v5b-value-renaming-580abae854514a7fb49fe1f702f4b50d/summary.json.
Summary SHA256: eec24c37d318d0634623185193b50a4a7e4fb82abd6abe350a4712f807d59961.
Own32 and focused4941 PASS;706 source pins/1323 inputs;36 parent archives verified.
Original C309 normal totals720 reconstructed. Full 256-class argmax and original split/score
definitions preserved. persisted_value_renaming=PASS; diagnostic_complete=True;
run_execution_valid=True; tracked tree clean; scientific HEAD preserved.
No new model calls,training updates,model state loads or checkpoints.
Log transport changed latest.json and latest.log only.

## Deciding observed aggregates
15 fixed C309 models,4 lengths,3 name profiles,288 ordered logical rows per block:
51840 original hard answers. Twenty-two changed-input bijections per row:
1140480 directed dependent comparisons. Identity controls:51840/51840 equivariant.
Absent-value swaps:51643/51840 equivariant,197 violations; these do NOT change inputs.
Changed-input comparison by arm (equivariant/total):
full_train378610/380160,1550 violations;
core_frozen374320/380160,5840 violations;
core_slow377774/380160,2386 violations.
Total1130704/1140480 equivariant;9776 violations.
Cross-split TRAIN->HOLDOUT:272840/276480 equivariant,3640 violations;
HOLDOUT->TRAIN mirrors these directed comparisons,not independent observations.
Within TRAIN:483756/483840; within HOLDOUT:101268/103680.
The failing five-character seed309002 has,by arm:
full18502/19008;frozen16912/19008;slow18178/19008 equivariant.
Fixed/lowered-core policies rescue other seeds but both still fail309002.
Equivariance and correctness reported separately:consistent wrong and non-value-class outputs
remain wrong. These are dependent observations,not statistics from independent 1.14M trials.
C310's PASS is audit integrity,NOT model quality and NOT a cure for C309 failures.

## Next boundary
The next diagnostic should localize ORIGINAL wrong answers by named context and ordered
value pair,especially held-out value-pairs for309002. Preserve exact same saved models/outputs,
original TRAIN/HOLDOUT and all masked/full gates. Analyze persistence across2/3/4/5 for each
same logical question and classify wrong outputs (other fact,unmentioned digit,non-digit).
Do not add training,hyperparameter changes,seeds or new model forward. This is a proposed
question,not C311 registration. Author/review committed next-C bytes before activating.
