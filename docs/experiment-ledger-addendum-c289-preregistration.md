# C289 preregistration — early auxiliary withdrawal with concurrent anchors

Experiment:C289-v5b-early-pair-withdrawal. Stage:V5-B-EARLY-PAIR-WITHDRAWAL.
Acceptance base:4acd3873a4f524ceb3080aab10653cd13caaa1c4.
C288 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C290 NOT REGISTERED.

## One scientific question

Can restricting the existing pair-assignment auxiliary to updates1..400 retain fitted-query gains
without the reliable four-character transfer regressions of always-on auxiliary training?
Compare the candidate with both a concurrent always-on schedule comparator and a CE-only anchor.
C288 showed fitting improvement and mixed transfer effects;it does not prove that late auxiliary
pressure caused its failures. Withdrawal may be ineffective if the auxiliary is already saturated.

## Parent identity and writer semantics

C288 execution:f43618b6bb6fcc1ad4a4a4b928992adce29f4e41.
Published log:eb9f27224460ad614e80b5feb23a5411d8ea42d6.
Summary:runs/c288-v5b-pair-assignment-f6a7427e94c44fc7b818f8cd18626562/summary.json.
Summary SHA256:2a15fbf6c5e697d5e226bdae5a5b2f243f43625b29255839100d2f05ce24fbc0.
Direct source blob:f7f9c73565828e23533efd188f25009e5e4b3d50.
Fifteen ordered summary hashes:C288 down to C274. Every hash is independently checked before dispatch.
All8 parent artifact hashes/sizes are sealed in PARENT_ARTIFACTS and in the C288 acceptance addendum.

Use C288.verify_artifacts(parent_dir,fourteen ancestor paths,accepted execution_HEAD),not a similarly
named older loader. It returns payload and metrics;it reconstructs all old task-keyed raw outputs,
CE/pair/total histories,matched pairs and60 final partitions. Require FAIL,candidate_gate=False,
all_replays/all_pairs_matched=True and exact10 seed_results:quad3/1;trained-length TRAIN direct3/5;
seen HOLDOUT direct3/3. The candidate trained-length TRAIN answers are perfect but its gate is1/5.
C289 does not use parent checkpoint weights for initialization. Parent reconstruction forbids
Module calls,load_state_dict and torch.save. Reading saved logits/provenance is permitted.

C288.context supplies C287 diagnostic helpers,C284 evaluate/replay,C283 transfer scoring,C282
training tables,and pinned core/reader/factory dependencies. C289 owns its identities,schedule,
objective schedule,15-state persistence and analysis;do not apply C288.analyze to C289 records.
C287 normalize_task/partition are identity-agnostic helpers;its identity-bound analyze is not used.

## Fixed three-arm comparison

Fresh seeds289001..289005;arms in order ce_only,pair_always,pair_early.15 models total.
All use actual C278 all-token MeanFinalDualReadout,14256 parameters,48-token context,CPU float64.
Construct one initialized model per seed,then deep-copy twice. All initial fingerprints/state keys
match with independent parameter storage. No new layer,trainable scalar or inference-time metadata.

Use normal mixed2/3 C282 TRAIN tensors[2,3,192,48]. Four-character,HOLDOUT and masked examples never
enter the optimizer. Logical data1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
triple432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73;
quad86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b.

96 intact query pairs from192 logical TRAIN rows.200 epochs x4 batches x48 rows.
randperm96(seed+289000+epoch);profile=epoch%3;length=epoch%2;fit RNGseed+290000 reset per arm.
Every logical row200 exposures,100 for each trained length. Length/profile update matrix:
[[136,132,132],[132,136,132]] in all3 arms. No early stopping,seed substitution or data selection.

## Objective schedule and optimizer continuity

For each existing query pair with distinct TRAIN labels y0,y1 and logits z0,z1:
correct=z0[y0]+z1[y1];swapped=z0[y1]+z1[y0];Lpair=mean softplus(1-(correct-swapped)) over24 pairs.
CE is mean cross-entropy over48 rows. Same formula and margin1 as C288;runtime preflight compares
new objective outputs with the actual C288 helper. Weight is assigned before each optimizer update.

|arm|updates1..400|updates401..800|
|---|---|---|
|ce_only|CE|CE|
|pair_always|CE+0.25*Lpair|CE+0.25*Lpair|
|pair_early|CE+0.25*Lpair|CE|

Only pair_always versus pair_early differs after400;CE-only is a same-cohort reference,not evidence
of a common prefix. All models use a single continuous AdamW optimizer for800 updates,lr.005,
betas.9/.999,eps1e-8,weight_decay0,global gradient clip1. No optimizer reset or LR change at401.
No intermediate checkpoint write. Record a step400 weight fingerprint for every state.
Require pair_always and pair_early step400 fingerprints and first400 CE,pair,total histories to
match exactly. Compare all3 initial states,logical batches,rendered schedule and actual LR history.
Prefix mismatch invalidates execution;it is not a scientific negative. Do not weaken these checks.

Compute CE and pair terms in all arms for diagnostics. When weight0,use exactly CE and its gradient,
not a detached or modified objective. The disabled pair term is not backpropagated. No additional
forward or training example. Record all800 actual weights,LRs,CE,pair,total values;reconstruct every
total at1e-12 tolerance. Check optimizer step state continuity in authoring tests across400/401.
Loss histories are pre-update minibatch values,not full-dataset loss or model-selection criteria.

## Frozen evaluation and interpretation

Freeze after800 updates,evaluate unchanged two/three/four tasks,then strict-load final weights and
replay all3 with C284 helpers. New schemas:fold-c289-early-pair-models-v1 and fold-c289-early-pair-eval-v1.
C289.analyze reconstructs full metrics,90 final model/task/split partitions,and360 paired normal/
collapse totals:pair_early versus ce_only AND pair_early versus pair_always,all5 seeds/all3 tasks.
Each contrast names its comparator explicitly. Direct TRAIN/HOLDOUT and full task gates remain distinct.

Primary absolute PASS iff all FIVE pair_early final states pass every FOUR-character fixed criterion.
Thresholds unchanged:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
passed=quad_pass;two/three/all-task and fitted/seen-HOLDOUT direct gates are descriptive and reported.
An absolute PASS is not comparative superiority. Pooled accuracy cannot override a seed-level miss.
Retaining fitting benefits requires comparing fitted metrics with BOTH concurrent anchors;report
regressions even when transfer improves. No retrospective removal of failed states or best checkpoints.

Withdrawal changes the time allocation and total auxiliary gradient exposure together. This is a
fixed training-policy test,not a proof of a unique late-pressure mechanism. Margin saturation can
make the intervention inert. A negative result must not trigger within-C289 switch/weight tuning.
New seeds mean C288/C289 rates are not one-factor before/after estimates. All prior verdicts remain.

## Workload and persistence

15 fresh models,12000 updates,576000 training row presentations.800 updates/model in every arm.
Per model881 train/evaluation forwards+81 replay=962;totals14430 forwards,809280 row presentations,
57720 core calls. One15-state checkpoint bundle write/load;15 strict state loads;new writes1;network0.
The third arm increases total scientific workload50% versus C288,not per-arm training budget.
Auxiliary arithmetic/recording still costs time/memory;equal model-forward counts are not equal cost.
Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json. All generated artifacts
remain local-only;only console logs are published by the dedicated publisher.

## Protection and authoring gates

OWN6:source,test,runner,launcher,preregistration,design. Source580=574+6;
protected1041=1026+9 new parent inputs+6 OWN;inherited dependency-union65.
Direct repository import:C288. Reachable C287/C284/C283/C282/C278/C269/C267 and core helpers are
inherited source-pinned/protected. Accepted sources/tests and both existing dispatchers stay unchanged.
Own48;modules174;loaded4206;focused4205. Sole inherited exact C204 exclusion unchanged.
Manifest SHA256:48b33a7ed29cf9ded858753d5f64210006f559ef428c167e912621a71896ae21.

Commit and re-fetch all OWN6 for independent review before activation. Validate real parent data,
actual three-way initial models/training tables/pairing/objective equivalence,own48 and actual full
focused4205 before scientific execution/logging. Dispatcher/launcher/runner use PowerShell ParseFile.
Operational failure skips science/publish. Scientific integrity failure retries SAME C289.
Valid all-five miss is ACCEPTED VALID NEGATIVE. Gate F stays NOT PASSED. C290 NOT REGISTERED.
