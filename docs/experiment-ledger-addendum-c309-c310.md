# C309 formal acceptance — valid negative

C309 ACCEPTED VALID NEGATIVE. New core_slow cohort passes4/5,not registered5/5.
C308 remains ACCEPTED PASS within its original bounded capability scope. Gate F NOT PASSED.
C310 NOT REGISTERED in this acceptance commit. Do not rerun C309 or change its threshold.

## Evidence identity and execution validity

Scientific execution HEAD:a38c6ff864ab40efa74397017cfeec9f5628ca11.
Published log commit:c3935db64960b7e90325672aa880318a6eed77e2.
Metadata log SHA256:6600f5af0bb59d36365d45544457e25ec2bae070795b2fd22319f0acac378cda;810894bytes.
Publication changes only docs/experiment-run-logs/c309/latest.json and latest.log.
Summary:runs/c309-v5b-core-lr-replication-e24b3b724e47415eae204d3084a68185/summary.json.
Summary SHA256:c8a1a2bd3d6ad4e4d6f714b38af3ce8424d314d1f5771b5fca578d49df37066c.
Manifest:9350f7a5ec4e91a3292f6ecce041bc3ec09f1fa1a8372a4178b58d0ceb4df74d.
Own32/focused4909 PASS;full suite825.948s;source700/protected1309.
All15 fits and strict replays complete. all_groups_matched=True;
persisted_core_lr_replication=PASS;tracked tree clean;execution HEAD preserved;run_execution_valid=True.
Scientific FAIL is a capability negative,not invalid execution. Evidence reviewed is the immutable
published receipt/postcheck,not independent execution of the user's local model artifacts.

## Deciding results

Order full_train/core_frozen/core_slow:
length2:4/4/4;length3:4/4/4;length4:3/4/4;length5:3/4/4.
All-length pass3/4/4. All15 fitted_train_direct_pass=True.
Trained-length HOLDOUT direct3/4/4. Candidate and frozen pass the same four seeds.
Against full:both-pass3,candidate-only1,control-only0,both-fail1.
Against frozen:both-pass4,candidate-only0,control-only0,both-fail1.
309005 is rescued by frozen/slow.309002 fails every arm's five-character gate.

309002 HOLDOUT correct at lengths2/3/4/5(out288):
full_train288/288/285/277;
core_frozen261/262/254/239;
core_slow276/276/275/269.
All three fit normal TRAIN2/3/4 perfectly576/576. At5,all three TRAIN-valued partitions575/576.
Thus the failed slow/frozen seed already has seen-length value-HOLDOUT errors,and ordinary training
is better on this particular seed even though its cohort pass count is lower. No universal rescue.

## Interpretation and next boundary

C308's all-five success did not recur in the new cohort. There is no pass-count superiority of
slow versus frozen in either cohort. Preserve old and new verdicts separately;no pooling to pass,
no extra seed cohorts until success,and no immediate LR-ratio search.

A next separately registered saved-output diagnostic will test value-renaming consistency:holding
names,query and fact order fixed,do predictions transform with a bijective relabeling of values0..3?
The existing dataset contains every ordered distinct value pair across TRAIN/HOLDOUT,so these
comparisons can use saved logits only. Keep original splits and gates. Distinguish changed-input
renamings from identity and permutations that only swap the two absent values. Equivariance alone
is not correctness:always choosing the other fact or a constant non-value byte can be consistent
and wrong. This is descriptive evidence,not a hidden-mechanism diagnosis or production change.
C310 requires its own code/tests/preregistration/review before activation.
