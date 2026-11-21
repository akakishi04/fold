# C313 formal acceptance — six-character valid negative

C313 ACCEPTED VALID NEGATIVE. Prospective primary random_pairs passes2/5 at six,not5/5.
The fully retained value_balanced comparison passes1/5. C312 remains valid negative;
C308 bounded PASS,C309 negative and Gate F NOT PASSED remain unchanged.
C314 NOT REGISTERED in this acceptance commit.

## Evidence and execution validity

Scientific execution HEAD:bc6a226b8605b6ae04e64d46a387487533c0bdc0.
Published log commit:aef7187d19ed49b3ba0f29b5621fc675c4365b2d.
Log SHA256:723b92f31e3ac8737ad57c89645e918be02740e1a6624adaaa6e390635826c9f.
Log bytes:768695. Publication changes only C313 latest.json/latest.log.
Summary:runs/c313-v5b-frozen-six-8ef41237b7f84f148a0dcdce4b9aed21/summary.json.
Summary SHA256:adfeb06f6db5b77feb172b8ede1f3bf7032c8ca35b299d7ecc692baeca097c97.
Manifest:f6e02599e4704457781f1ac49272a0a8d50d9c40524d66d4bcfb173e1cf86cca.
Own32/focused5029 PASS;source724/protected1357;all10 frozen evaluations completed.
All before/after original2..5 replay errors are0.0;all_replays=True.
persisted_frozen_six=PASS;run_execution_valid=True;tracked tree clean;HEAD preserved.
Training0;2430 model forwards include old-before/six/old-after. Do not rerun C313.

## Deciding metrics

Random_pairs six passes:312004,312005. Value_balanced:312004 only.
Five->six pass counts:random5->2;balanced4->1. No primary substitution.
Per seed312001..312005,normal six TRAIN/HOLDOUT correct counts (denominators576/288):
random:(561,278),(573,286),(576,287),(576,288),(576,288).
balanced:(570,281),(559,274),(569,282),(576,288),(574,286).
Random normal errors31,all new relative to five (18TRAIN-value,13HOLDOUT-value).
Balanced normal errors61:58new,3persistent,0recovered. All3persistent are312002.
Pooled accuracy does not replace unchanged local/masked gates;some nonperfect TRAIN-value
partitions still pass their full local criteria. TRAIN-value six is not six training.

## Interpretation and next boundary

At frozen weights and unchanged64slots,the five-character result does not extrapolate
uniformly to six. Failures are not baseline-reproduction or checkpoint failures.
No inference yet about a particular language,name family,attention mechanism or context
boundary: the maximum Japanese input uses63/64 slots,but that alone is not causal evidence.
A next separately registered saved-logit diagnostic should locate five-to-six new errors
by language/name profile/split,with paired correct-answer margins and exact original-count
reconciliation. Keep all10 models and failed states. No training,new forward,model changes,
threshold relaxation or answer repair. Language,byte length and final positions co-vary;
observational localization cannot isolate their causal contributions.
