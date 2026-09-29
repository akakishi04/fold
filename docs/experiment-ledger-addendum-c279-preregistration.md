# C279 preregistration — saved mean/final dual-query failure-profile audit

Experiment:C279-v5b-saved-dual-failure-profile-audit.
Stage:V5-B-SAVED-DUAL-FAILURE-PROFILE-AUDIT.
Acceptance base:b3745f7d90565297cd4d19024d7da4fd62954251.
C278 ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C280 NOT REGISTERED.

## One scientific question

For accepted C278 saved outputs,which fixed gate criteria remain responsible for the
mean_final_dual three-character failures by seed,split and profile,and is the residual failure
specifically concentrated in shared_suffix2 mask sensitivity/two-order behavior rather than direct
answer discrimination?

## Parent evidence

C278 execution:ca6e45cc90b3b48e3d56c10acde72e35574878fd.
C278 summary:runs/c278-v5b-mean-final-dual-c1d5206c6c6a48ab98acd15c5cb8aa71/summary.json.
C278 summary SHA256:557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b.

Require C278 status FAIL,candidate_gate=False,
seed_pass_counts mean_span0/mean_final_dual0,
two_char_pass_counts5/5 each,triple_pass_counts0/5 each,
all_pairs_matched=True and all_replays=True.

Required C278 artifact SHA256:
-architecture-plan.json 791f287f21bcadd6c708496cd6922a2ef82a2ab94d2cf12ab5c3d669e1917dec
-dataset.json 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1
-triple-dataset.json 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73
-trained-models.pt a86f34ed93dd8b3d0f2e46e960f134571223f2146b31763202b4f11b778f52d5
-evaluations.pt 1ee106c701ee4ca6048c6bc9200bee343f57a7cfe88d2c201aa920ada8c2bfdc
-measurements.json ae12d78b16787622efc62206775a7ec7e9e021a8085b7c42a8bea8efbb90e24f
-validation-summary.json 01a2dd82e73cfcc06feffa14b0edb5c5f2df7af0f0366f5b0cc3142e3862678c

Ancestor summary SHA256:
-C277 ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13
-C276 6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f
-C275 1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb
-C274 0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0

## Diagnostic contract

No new model,training,inference,checkpoint,seed,threshold,dataset or optimizer.
Reconstruct every accepted C278 answer-cell and two-order fixed criterion from saved evaluations
with torch.nn.Module calls blocked.

Persist:
1.all triple criterion failure counts and candidate-minus-control deltas;
2.shared_prefix2 HOLDOUT criterion deltas;
3.shared_suffix2 TRAIN and HOLDOUT criterion deltas;
4.per-seed triple criterion deltas for278001..278005;
5.signed negative-margin ranges and exact failed records.

Thresholds remain accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Formal PASS means only diagnostic integrity. capability_gate_applicable=False.

## Workload and persistence

model_forward_calls=0;row_presentations=0;core_forward_calls=0;train_steps=0;
new_checkpoint_writes=0;model_state_loads=0;network_calls=0.

Artifacts:
-audit-plan.json
-failure-profile.json
-validation-summary.json
plus summary.json.

## Protection/runtime

Expected source pins520;protected inputs916;direct deciding dependencies55.
OWN6 benchmark/test/runner/launcher/prereg/design.
Own24;modules164;loaded3862/focused3861.
Sole inherited exact C204 exclusion unchanged.

Manifest SHA256:daeea4cfcf5083ec9a5237ea092f0c11ac7ab3cf38b76e9cdf62f60c4fea1af7.
Registration cardinalities are manifest-derived at runtime.
C278/C277/C276/C275/C274 summaries are modeled independently.
Parent verification blocks neural Module calls.

Use Validate->Execute. A runtime integrity failure retries SAME C279.
C280 remains unregistered until C279 is judged.
