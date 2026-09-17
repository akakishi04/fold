# C175 acceptance — frozen predictions versus TRAIN-only frequency reference

Judged 2026-09-17 JST. Repository akakishi04/fold, branch feat/sft-target-loss.
Read experiment-ledger-addendum-c175-preregistration.md and the conversation protocol.

## Formal verdict

**C175 ACCEPTED PASS. C174 remains ACCEPTED PASS. Gate E NOT PASSED.**
C176 is NOT REGISTERED at this acceptance-only boundary. No historical result is revised.
C160/C168/C169 remain ACCEPTED VALID NEGATIVE. No retraining or threshold change occurred.

## Execution and artifact identities

Execution HEAD d54a4921a4e90ea58d72cd66988f946e67c1031d.
Source/artifact precheck PASS; 973/973 focused tests in 18.873 seconds; all three audit
phases completed. 311040 saved model decisions reaggregated, 81 TRAIN-only blind keys,
51840 reference predictions. Benchmark training, model forwards, checkpoint deserializations,
fresh seeds, actual acquisitions, evidence writes and network calls are all zero.
Production runtime unchanged; gate_e_candidate false. Runner postchecks report protected
inputs preserved, tracked tree clean, execution HEAD preserved, run_execution_valid True.
64 input paths and 48 historical source pins are recorded. Existing C145 warning was in a
passing regression and is not an invalidity. Audit wall clock 6.262705500004813 seconds is
not model inference latency.

Parent C174 summary SHA256:
3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36.
C175 summary:
runs/c175-v5e-frozen-predictions-9c1b782f75bc42dbae6c3b841fb98163/summary.json
SHA256 d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722.
Uploaded UTF-8 log 235289 bytes:
34830743bf4da903f7a02e5816d08e21ecc68ee43dd65433b92158166f82209c.
Scientific manifest 51c7b72eb8496118185ec9ab370f068902f312b332855abc479be00a5ffc9478.
Written audit-plan.json 5830 bytes:
31fcb10fec9562f6f2a83f516d343c1b73500a4060872064b8e624a0637152c9.
audit-details.json 218224 bytes:
e3b0590fec5e46ad8463a897ca06775514df3ee7c3967dc304b8af0411e12ef9.

Reviewer independently reconstructed the complete summary JSON hash and recomputed
96 supplied confusion-matrix score tables, group means/sums, all 12 matched-pair rates
and the three deciding differences. All agree with the log. The 81-key detailed table,
C174 NPZ/prediction/checkpoint artifacts and user-machine regression were NOT independently
read or rerun by the reviewer. Local runner verification and independent summary arithmetic
are distinct evidence levels. No missing detailed artifact is claimed independently audited.

## Deciding metrics

Primary is equal mean balanced accuracy over the same four PILOT_EVAL semantic groups.
TRAIN-only frequency reference primary 0.6927057895807895; ordinary accuracy
0.7275436355896125; SUFFICIENT recall 0.791814946619217; NEEDS recall 0.5641025641025641.

| Seed | Frozen TASK_VISIBLE primary | Difference from reference | Sufficient recall | Needs recall |
|---|---:|---:|---:|---:|
|174001|0.7217363934291018|0.029030603848312242|0.8167259786476868|0.584841628959276|
|174002|0.7267349717219510|0.03402918214116146|0.8198398576512456|0.5855957767722474|
|174003|0.7383088135822511|0.045603024001461545|0.7743179122182681|0.6504524886877828|

All three strictly exceed the registered reference and both class recalls exceed 0.5.
No averaging away a failed seed. C174 predictions are unchanged; C175 does not improve them.
Group 3 still loses to this reference in all three seeds; other groups improve.
The reference is not uniformly stronger than the learned ablation (especially seed174003).
It removes optimization uncertainty in TRAIN empirical majority, NOT all possible blind
baselines and NOT optimization for PILOT_EVAL macro balanced accuracy.

## Batched secondary findings

In PILOT_EVAL, missing-count0 has1856 all-sufficient rows and missing-count4 has116
all-needs rows. Both extremes are classified correctly by all six models. Their balanced
accuracies are null because one class is absent; they were not discarded from the main gate.

| Seed, TASK_VISIBLE | Needs recall with1 missing (768 needs rows) | Sufficient recall with3 missing (312 sufficient rows) | BA with2 missing | Matched-visible both-correct |
|---|---:|---:|---:|---:|
|174001|73/768 =0.0950520833|11/312 =0.0352564103|0.5888991013|25585/165552 =0.1545435875|
|174002|24/768 =0.0312500000|7/312 =0.0224358974|0.6011029412|23176/165552 =0.1399922683|
|174003|230/768 =0.2994791667|11/312 =0.0352564103|0.5939031863|35258/165552 =0.2129723591|

All learned blind controls have matched-visible both-correct0, as expected for a fixed
prediction on the identical blind input. Mixed blind keys64. Pair counts share rows and
are correlated, not165552 independent experiments or one-edit interventions. A nonzero
pair rate supports some syntax-dependent discrimination, not complete logical reasoning
or a random-chance comparison. The visible models still miss most count1 critical facts
and nearly all count3 short-circuit sufficient cases.

The same weakness exists on TRAIN: count1 needs recalls0.1220128676/0.0613511029/
0.3710937500; count3 sufficient recalls0.0950413223/0.0795454545/0.1188016529.
This is not exclusively a held-out-group transfer problem.
TRAIN label counts [SUFFICIENT,NEEDS] by missing count are:
0:[8384,0],1:[12416,4352],2:[6048,6528],3:[968,3224],4:[0,524].

## Interpretation and next-design rationale

Claim: all three frozen visible models beat the specified TRAIN-only blind-majority
comparator on the reused pilot endpoint, and show some correct syntax-dependent switching.
Non-claims: independent replication, calibrated confidence, reliable necessity routing,
selected fact/tool, learned proof generation, FOLD-core superiority or final Gate E PASS.
These are the same four pilot groups selected for development; no new independent holdout.

Observed error patterns are compatible with reliance on missing-count class frequency.
That is a hypothesis about training incentives, not a demonstrated internal causal mechanism.
Neither scaling model width nor extending training is justified by this audit alone.
A targeted next intervention should hold the model, rows, split, budget and paired batches
fixed, and change only TRAIN loss weights conditional on missing count and class. This
would test the training-incentive hypothesis without correcting inference or reusing a
lucky C174 checkpoint. It must be separately preregistered; no C176 result is implied here.
