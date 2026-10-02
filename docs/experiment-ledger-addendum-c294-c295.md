# C294 acceptance — saved support/choice diagnostic

C294 ACCEPTED PASS (diagnostic integrity only). C293 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C295 NOT REGISTERED in this acceptance commit.
Scientific execution HEAD:dead7ca153a8aadb6f30135f47a59981e4b4dfcf.
Published log commit:de959a8147df888a6d51234fad7971f4593d25a2.
Publication changes only c294/latest.json and latest.log. Metadata log SHA256:
0e1ea3730303ce5c25706fdbfce10e49b9c03c9705e27063ae4f0f44fb601d6e;775517 bytes.
Summary:runs/c294-v5b-support-choice-79d31882e59f46fe933bb7e863bad8e2/summary.json.
Summary SHA256:abdf1b71f56e3f452d3955277a659722ca38f95a47be1dc6ca5330e688e37e10.

## Validity

Own32 and focused4389 passed;the log reports4389 tests in277.148s and preflight PASS.
Source610/protected1106;manifest e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6.
Diagnostic complete;persisted_support_choice_audit PASS;tracked tree clean;execution HEAD
preserved;run_execution_valid=True. New scientific model forwards/training/state loads/checkpoint
writes are0. The user repeated the old command after publication;RESULT_ALREADY_PUBLISHED correctly
prevented a second execution. That invocation did not mean the first run was absent or failed.

Outputs sealed by the exact summary:
-audit-plan.json:2053 bytes;e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6.
-support-choice-report.json:25996203 bytes;878b04c53585d880990edc0180627e52b68efbdb7da8cc73ff88c41f75bc4491.
-validation-summary.json:101776 bytes;820d37672cd1333ce613dd9c9f5d70a7a55e8fcca128796fb06b7aa5dfaf124f.

## Deciding observations

For support_weighted seed293004 HOLDOUT:
-two_char:full correct259/288;conditional276/288;outside_correct_choice17;
 outside_wrong_choice12;other_fact0.
-triple:full253/288;conditional269/288;outside_correct_choice16;
 outside_wrong_choice17;other_fact2.
-quad:full239/288;conditional255/288;outside_correct_choice16;
 outside_wrong_choice24;other_fact9.
Thus for quad40 outside-support errors,24 also have the wrong within-fact ranking;oracle support
would still leave33/288 mistakes. This is not a deployable decoder or a new capability result.
The same candidate's quad TRAIN-value split has26 other-fact errors and no outside-support errors.
CE on293004 has quad HOLDOUT200/288 full and243/288 conditional,with43 outside_correct_choice,
28 outside_wrong_choice and17 other_fact. Scaling CE has190/288 full and220/288 conditional.
The conditional view does not universally resolve residual errors.

Parent C293 gates remain quad2/1/2 for CE/scaled/support. No threshold,cohort or prediction changes.
Do not infer a specific hidden cause from these descriptions. The data and models are dependent,
and the oracle-support accuracy is not a new model capability. C294 does not select a new loss.

## Next controlled question

Before further loss or decoder changes,test whether the fixed800-update budget is a material
limitation for ordinary CE. Proposed C295 uses fresh seeds and the SAME uninterrupted optimizer
trajectory,with predeclared snapshots at800 and1600 updates. The second half repeats the same
normal length2/3 TRAIN corpus;no new lengths,labels,HOLDOUT or masked inputs enter optimization.
Evaluate both fixed snapshots after training,with independent strict replay and the original gates.
This is explicitly a doubled per-model training-budget comparison,not equal-compute superiority.
No best-checkpoint selection,adaptive stopping or failed-seed filtering. It does not prove C294's
errors arose from undertraining. It directly measures the chosen fixed-budget extension policy.
C295 needs separate preregistration,code/tests and committed-byte review. C296 NOT REGISTERED.
