# C283 acceptance and C284 maximum-training-length-matched comparison

## Formal verdict

C283 ACCEPTED VALID NEGATIVE. The frozen mixed_length arm passes3/5 complete four-character gates;
two_char_only passes0/5. The registered all-five candidate gate is false. Relative improvement is
real in this cohort but does not satisfy that gate. C282 remains ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. No model or seed is selected for promotion.

Scientific execution HEAD:24c4acd44905e1d3c4d2a019214eb588d72f9a93.
Published log commit:aedfa69557782b7484ee71128b08213a27d8798d.
Log SHA256:3ee72ebe5b9a2ace70fdad2e6831ca01ab85689606bf43a265420d883f3ad5dd;834360 bytes.
Summary:runs/c283-v5b-frozen-four-bacee738e5a04007ae0f0f3093b0f5a7/summary.json.
Summary SHA256:609718db24ca6e3eda4f8916f04f56b24bff3621ddca4ebe136209617fad4949.
Manifest SHA256:e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4.

## Execution validity

Published own32/focused3981 PASS;authoring_runtime_preflight=PASS.
Source544/protected964 registration and dataset/scorer checks passed. All10 frozen C282 states
were strict-loaded and evaluated through anchor(two+three)->novel four->restore(two+three).
all_replays=True;all_weights_preserved=True;persisted_four_character_scores=PASS;
tracked_tree=clean;execution_HEAD=preserved;run_execution_valid=True;scientific_status=FAIL.
Scientific workload:1350 model forwards,129600 row presentations,5400 core calls,10 strict state
loads,one checkpoint bundle load,zero training/optimizer updates/new checkpoint writes.

## Deciding metrics

Complete four-character gates:control0/5;candidate3/5.
Mixed states282002/282003/282004 pass;282001/282005 fail. All five control states fail.
Aggregating the60 published matched contrast rows (not independent statistical samples):

|split/profile|control correct|mixed correct|control collapse|mixed collapse|
|---|---:|---:|---:|---:|
|TRAIN quadrupled|941/960|960/960|13|0|
|TRAIN shared_prefix3|906/960|959/960|49|1|
|TRAIN shared_suffix3|719/960|956/960|188|3|
|HOLDOUT quadrupled|467/480|465/480|7|0|
|HOLDOUT shared_prefix3|447/480|457/480|13|1|
|HOLDOUT shared_suffix3|325/480|469/480|77|0|

Total normal correct3805/4320->4266/4320;collapse347->5 (2160 query pairs/arm).
HOLDOUT normal correct1239/1440->1391/1440. TRAIN/HOLDOUT label the inherited value split;
ALL four-character prompts were unseen in optimization by both arms.
Per-seed normal correct/collapse control->candidate:
-282001:740/864,92 ->818/864,1.
-282002:792/864,59 ->862/864,2.
-282003:766/864,41 ->864/864,0.
-282004:795/864,44 ->864/864,0.
-282005:712/864,111 ->858/864,2.
Every seed improves pooled normal accuracy and collapse;not every profile improves.
These pooled metrics do not replace cellwise accuracy,query-pair,mask-drop or two-order gates.

## Interpretation and non-claims

The learned mixed two/three-character regime transfers materially better to unseen four-character
names than the matched two-character-only regime in this bounded family. This supports a transfer
benefit of the regime,not yet a unique causal claim about diversity. Maximum training length also
rose from2 to3 and exposures were redistributed. Arbitrary length/name generalization is unproven.
C283 did not train on four-character examples. Do not relabel C282 as PASS,discard failed states,
relax the all-five gate,or extend context/training to repair these results.

## Accepted artifacts

-transfer-plan.json:e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4;3279 bytes.
-quad-dataset.json:86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b;172066 bytes.
-eval-outputs.pt:283d3015f09a79bbab180bde7caa3a24381239b7e384b70745152c7471bf3ead;265676521 bytes.
-measurements.json:212155b8bc11906bd80ac3dc6ba3d397c6d7c8cc4a1169bdee75c319ae33e807;264243 bytes.
-validation-summary.json:c552ae8782437365eb7cc0bfb4049be507010c67c43280c79ed29a74c57c1928;12038 bytes.

## Next question, not activation

At matched maximum training length3,architecture and800-update budget,does mixed two/three-character
training improve unseen four-character transfer over THREE-character-only training?
C284 should use fresh paired seeds284001..284005,actual C278 all-token MeanFinalDualReadout in both
arms,identical logical TRAIN batches,CE/AdamW lr.005,and no four-character optimization.
Control allocates200 exposures/row to length3;candidate100 each to lengths2/3. Maximum length is
matched;exposure allocation remains part of the intervention. Evaluate all three tasks,with the
unchanged all-five FOUR-character gate primary and two/three task gates descriptive. Compare paired
seed and profile results separately from candidate absolute PASS. Gate F remains NOT PASSED.
No C284 activation until separate preregistration,implementation,committed-byte review and runtime
Validate. C285 NOT REGISTERED.
