# C288 acceptance and next bounded question

## Formal verdict

C288 ACCEPTED VALID NEGATIVE. Scientific execution completed correctly;the preregistered
ce_pair_assignment four-character all-five gate missed at1/5 versus ce_only3/5.
Gate F NOT PASSED. Do not rerun C288 or change its seeds,objective,thresholds or prior verdicts.

Scientific execution HEAD:f43618b6bb6fcc1ad4a4a4b928992adce29f4e41.
Published log commit:eb9f27224460ad614e80b5feb23a5411d8ea42d6.
Log SHA256:b5949f17ee4d3f269f52dd6c00e0756a89cae6a9f1b2d02caff28a6f949d9249;975379 bytes.
Summary:runs/c288-v5b-pair-assignment-f6a7427e94c44fc7b818f8cd18626562/summary.json.
Summary SHA256:2a15fbf6c5e697d5e226bdae5a5b2f243f43625b29255839100d2f05ce24fbc0.
Manifest SHA256:44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5.

## Execution validity

Published log has own40 PASS,focused4157 PASS,authoring_runtime_preflight=PASS,source574/protected1026,
all10 trained states,strict checkpoint replay,persisted_pair_assignment_scores=PASS,tracked_tree clean,
execution_HEAD preserved and run_execution_valid=True. scientific_status=FAIL;candidate_gate=False.
Registered work:8000 updates,384000 training rows,9620 forwards,539520 row presentations,38480 core calls,
one10-state bundle write/load,10 strict state loads. Scientific failure is not an operational failure.
C288's verifier reconstructs task metrics,objective histories,matched initial states/data/LR and60
final TRAIN/HOLDOUT partitions. The parent/source dependency chain remains pinned;accepted files unchanged.

## Deciding metrics

|gate|ce_only|ce_pair_assignment|
|---|---:|---:|
|four-character primary|3/5|1/5|
|two-character full|3/5|3/5|
|three-character full|3/5|3/5|
|all tasks full|3/5|1/5|
|trained-length TRAIN direct|3/5|5/5|
|trained-length HOLDOUT direct|3/5|3/5|

All five candidate states answer all576 normal TRAIN renderings correctly for EACH of lengths2/3,
with0 collapsed pairs. Their exact normal fit is not equivalent to HOLDOUT or length-transfer success.

|seed|ce_only quad|candidate quad|candidate seen-length status|
|---|---|---|---|
|288001|PASS|FAIL|both full tasks PASS|
|288002|FAIL|FAIL|TRAIN direct PASS;HOLDOUT direct FAIL|
|288003|FAIL|FAIL|TRAIN direct PASS;HOLDOUT direct FAIL|
|288004|PASS|FAIL|both full tasks PASS|
|288005|PASS|PASS|both full tasks PASS|

Thus candidate-only quad passes0;control-only passes2;both pass1;both fail2.

Pooled normal four-character totals,derived by summing all10 final_partitions per arm:
-ce_only3902/4320 correct,175/2160 collapsed pairs;HOLDOUT1103/1440 correct.
-ce_pair_assignment4011/4320 correct,90/2160 collapsed pairs;HOLDOUT1140/1440 correct.
Pooled accuracy/collapse improve despite worse strict seed reliability. Do not hide either result.

Candidate quad errors by seed:28800113/864;288002158/864;288003135/864;2880043/864;2880050/864.
Controls at288001/288004 were864/864. At288002 candidate fits both trained lengths perfectly but
HOLDOUT correct is134/288(two),135/288(three),130/288(four). At288003 candidate HOLDOUT improves
but still misses:159/288(two),151/288(three),153/288(four). No mask-only explanation rescues these.

## Interpretation and non-claims

The auxiliary objective successfully changes fitted behavior in this cohort but does not improve
the primary reliable transfer gate. It is not adopted as a completed generalization solution.
The result separates exact fitted answers from held-out values and from new lengths. It does not
prove a unique causal mechanism,universal overfitting,or inability of the architecture to generalize.
Five seed pairs and correlated cells do not establish a population effect. No post-hoc seed exclusion.
Neither pooled accuracy nor fitted5/5 can replace the preregistered quad gate.

## Accepted artifacts

|file|SHA256|bytes|
|---|---|---:|
|architecture-plan.json|44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5|3851|
|dataset.json|1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1|36024|
|triple-dataset.json|432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73|158236|
|quad-dataset.json|86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b|172066|
|trained-models.pt|15565c23d0fda2762e5ae954b439c36c0c0681df953fe21731cf38268f82fad8|1238007|
|evaluations.pt|2a5d1da162a46a1351dfc6232ce4172120c815321f810c774a816d9f54c235a2|159706383|
|measurements.json|94e1bad69c3dcdabee2604ead83b997abfefd11ecac19550225e5ebc07efe7fb|788605|
|validation-summary.json|460bd624531d3982a5c62170647380f8ee1fbe5b98574720280f9cd3ff5e1958|59413|

## Next question,not activation

Can restricting the same pair-assignment auxiliary to the first400 updates retain its fitting benefit
without the reliable-transfer regressions of always-on use? A new fixed-budget comparison should retain
CE-only as a concurrent anchor,always-on pair as the schedule comparator,and early-only pair as the
candidate,with15 fresh models across5 matched seeds. Same800 updates per model,data,LR,architecture,
margin1 and weight.25 while enabled. Always/early arms must have exact identical first400 losses and
step400 state fingerprints;no optimizer reset at the switch. All three arms receive the same data.
This tests a training policy,not a proven late-pressure cause;auxiliary saturation may make the switch
ineffective. The third arm increases total workload50% but preserves a same-seed no-auxiliary anchor.
A new preregistration and reviewed implementation are required. C289 NOT REGISTERED in this commit.
C290 NOT REGISTERED. Gate F remains NOT PASSED.
