# C282 preregistration — fixed-budget mixed-length training

Experiment:C282-v5b-mixed-length-training.
Stage:V5-B-MIXED-LENGTH-TRAINING.
Acceptance base:d54a8d5a775949ccb54dae6ebc9e934c7579c8f5.
C281 ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED. C283 NOT REGISTERED.

## One scientific question

At identical architecture and800 updates/model,does alternating two-character and three-character
TRAIN renderings improve both-task reliability over two-character-only training?
This is a training-distribution diagnostic. The mixed-length candidate sees the three-character
TRAIN names; a PASS is NOT unseen-length/name transfer and cannot promote Gate F.

## Parent evidence and identities

C281 execution:96d02062bf98cf32cfc5173c36db28bb00960f0d.
Published log:e3b5bd2e67da32ccfdff4f7503a99d364f4b76ec.
Summary:runs/c281-v5b-saved-support-audit-674eda46d9634e258004cabe55550065/summary.json.
Summary SHA256:f56aca6895d5acd69b3c7e557c04fdb95b2b5e13a8b0bfe56f7c6ea4d5878ea7.
Direct parent source blob:2e06703af5e187febc12dbf65f33e3a6a773e612.
Require PASS,diagnostic_complete=True,capability_gate_applicable=False,model_forward_calls0,
mask_only_cells0 in both arms/both tasks,and triple candidate accuracy-cell failures85.

Ordered eight summary hashes (C281,C280,C279,C278,C277,C276,C275,C274):
-f56aca6895d5acd69b3c7e557c04fdb95b2b5e13a8b0bfe56f7c6ea4d5878ea7
-00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db
-a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb
-557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b
-ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13
-6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f
-1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb
-0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0

C281 artifacts (SHA256;bytes):
-audit-plan.json:ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2;2603.
-failure-profile.json:dd80ffb33f3f98aa4b129cef5f5cec56562010b509f5933af41cf76e26d41420;1178793.
-validation-summary.json:1fc1e6e768b4ebfd1211974fae99dcb35603f2cf06b3e7d54fa7f8479426da2f;15880.
Parent verification uses C281.verify_artifacts(parent_dir,seven ancestor summaries,execution_HEAD),
with neural Module calls blocked. Parent artifacts are provenance only,not training checkpoints.

## Model, changed variable and held constants

Both arms use actual C278 MeanFinalDualReadout,all-valid-token support,shared mean/final query
weights,two separate softmaxes,post-retrieval averaging and unchanged post-core residual.
Both have14256 parameters and identical state keys;candidate is an independent deep copy of
control initialization. The unsuccessful C280 evidence-only mask is NOT adopted.
Fresh seeds282001..282005;arms two_char_only and mixed_length.

Use unchanged C267 logical data SHA256:
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
C270 three-character prompt dataset SHA256:
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.
Training tensors have shape[2 lengths,3 profiles,192 TRAIN rows,48 padded tokens].
Build them only from TRAIN rows and normal renderings using actual C267.render and C270.render.
HOLDOUT value assignments and ablated views never enter optimizer batches.
No entity/profile/length metadata is supplied to model.forward;only rendered tokens and zero task IDs.

## Fixed paired training budget

200 complete epochs;4 batches/epoch;24 complete same-facts/different-query pairs/batch;48 rows/batch.
Both arms use identical logical batches:randperm96(seed+282000+epoch);profile=epoch%3.
two_char_only always selects length0 (two characters).
mixed_length selects length=epoch%2 (length0 two characters,length1 three characters).

Per-length/profile update matrices (rows=two/three-character;columns=profile0/1/2):
-two_char_only:[[268,268,264],[0,0,0]].
-mixed_length:[[136,132,132],[132,136,132]].
Every logical TRAIN row has200 total exposures in both arms. Per-length row exposures:
control200/0,candidate100/100. This reallocates exposure,not adds optimizer work.
Distinct rendered-prompt diversity and repetition per length intentionally differ;this is part of
the coverage intervention,not an isolated architectural effect.

Both use mean CE only,AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,global gradient clip1.
Fit RNG(seed+283000) resets for each arm. CPU float64,2 threads,deterministic algorithms.
No early stopping,extra updates,seed replacement,best-checkpoint selection,auxiliary loss or LR sweep.

## Evaluation and interpretation boundary

Evaluate both final states using unchanged C267 two-character and C270 three-character scorers.
Retain every TRAIN/HOLDOUT split,profile,language,entity pair,fact order and mask view.
Thresholds:accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.
Primary PASS iff all5 mixed_length states pass both complete tasks. Control cannot rescue/fail it.
Report per-seed subgates and paired correct/collapse totals.

The control remains an unseen-three-character-length transfer baseline. The candidate's three-character
TRAIN prompts have been trained;its HOLDOUT prompts retain unseen value combinations,but not unseen
identifier length. No comparison may relabel candidate PASS as the original C270 extrapolation PASS.
Gate F remains NOT PASSED independently of this experiment's result.

## Workload, artifacts and protection

10 models;8000 updates;384000 training rows;9080 total model forwards;487680 row presentations;
36320 core calls;one10-state bundle write/load;10 strict state loads;new_checkpoint_writes1.
Per-model854 training/evaluation forwards plus54 strict replay forwards. Raw/argmax replay tolerance1e-9.
No network calls in science. Training-table hash and complete exposure schedule are recorded per fit.

Outputs:architecture-plan.json,dataset.json,triple-dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json,plus summary.json.
Schemas:fold-c282-mixed-length-models-v1 and fold-c282-mixed-length-eval-v1.
C280.replay_one is reused only for its schema-independent raw_two/raw_triple replay contract;
C282.analyze owns the new seed/arm/training-schedule validation and never calls C280.analyze.

Source pins538;protected inputs950;inherited dependency-union58;OWN6 unchanged pattern.
Own32;modules167;loaded3950;focused3949;sole inherited exact C204 exclusion unchanged.
All accepted files remain immutable. The child's only direct repository import is C281;actual
C280/C278/C270/C267 and other reachable helpers are covered by inherited pins/protection.
Manifest SHA256:291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de.

## Stop

Commit and re-fetch all OWN6 before independent post-authoring review and activation.
Validate(parent precheck,own32,focused3949) precedes science/logging. Validate failure skips science.
Scientific integrity failure retries SAME C282. Valid gate miss is ACCEPTED VALID NEGATIVE.
Do not revise length schedule,training budget,seeds or thresholds after results. C283 NOT REGISTERED.
