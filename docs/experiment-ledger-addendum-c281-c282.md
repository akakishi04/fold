# C281 acceptance and C282 length-coverage question

## Formal verdict

C281 ACCEPTED PASS for diagnostic integrity only. Gate F NOT PASSED.
Scientific execution HEAD:96d02062bf98cf32cfc5173c36db28bb00960f0d.
Published log commit:e3b5bd2e67da32ccfdff4f7503a99d364f4b76ec.
Publisher log SHA256:d64fb2bcc660d99f1294223c3b6c76cf0ca6bd5d57d274fe428282411f73b557.
Publisher log bytes:824953.
Git normalized log blob:aefe08ee62601e123b6df241240cf9318c6d8636.
Summary:runs/c281-v5b-saved-support-audit-674eda46d9634e258004cabe55550065/summary.json.
Summary SHA256:f56aca6895d5acd69b3c7e557c04fdb95b2b5e13a8b0bfe56f7c6ea4d5878ea7.

## Execution validity

Source/artifact precheck532/940 and sealed manifest
ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2 passed.
Own32 and focused3917 passed before science. All2160 fixed records and1080 paired records
were reconstructed from accepted C280 outputs. Neural Module calls,state loads and checkpoint
writes were blocked during parent reconstruction. Scientific training,model forwards,row
presentations,core calls,state loads,new checkpoint writes and network calls were0.
Persisted reconstruction passed;tracked tree clean;execution HEAD preserved.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False. C280 remains ACCEPTED VALID NEGATIVE.

## Deciding metrics

All triple fixed-criterion transitions (control=all_token_dual,candidate=evidence_only_dual):

|criterion|control failures|candidate failures|rescued|introduced|net candidate-control|
|---|---:|---:|---:|---:|---:|
|accuracy|92|85|23|16|-7|
|query_pair_accuracy|92|85|23|16|-7|
|evidence_drop|45|29|23|7|-16|
|query_drop|58|43|30|15|-15|
|two_order_accuracy|34|33|8|7|-1|

The answer/mask criteria have360 paired cells;two_order has180. Criteria overlap and must not
be summed as independent errors or samples. Triple answers:3960/4320 versus3973/4320;
collapse232/2160 pairs versus226/2160.

For shared_suffix2 HOLDOUT,accuracy failures27->22 (9 rescued,4 introduced),evidence_drop13->9
(6 rescued,2 introduced),query_drop16->10 (10 rescued,4 introduced),two_order12->9
(4 rescued,1 introduced). Answers395/480->402/480;collapse41/240->35/240.
For shared_suffix2 TRAIN,evidence_drop failures4->6,query_drop9->13,two_order4->7;
answers880/960->867/960 despite accuracy-cell failures21->20.

The apparent overall evidence-drop improvement is dominated by seed280004:
-evidence_drop failures43->25 at280004,net-18;
-other four seeds2->4,net+2.
Among the other four seeds,triple answers3381/3456->3374/3456;accuracy failures34->30,
with18 rescues and14 introductions. No seed is excluded from the primary result.

Most importantly,mask_only_cells=0 for both arms on both complete tasks. Every failing
answer cell also fails accuracy or query-pair correctness. Triple evidence_blind totals
are1080/4320 for both arms;two-character totals are also1080/4320 for both arms. These pooled
identities do not assert identical predictions or cell-level ablated accuracy.

## Scientific interpretation and limits

C281 does not support treating isolated evidence-dependence failure as the remaining sole
bottleneck. Direct answer discrimination remains unresolved,and the evidence-only support
intervention has heterogeneous rescues and regressions. It is not a general reliability fix.
Mask-only0 does not prove mask criteria redundant in every future model;it describes these
accepted outputs only. The280004/rest partition is post-C280 explanatory analysis,not a new
held-out test or authorization to discard280004.

After multiple query/support interventions under two-character-only training,the next useful
question is whether the same architecture can learn reliable three-character binding when
three-character examples are included in TRAIN at the same optimizer-update/row budget.
Use actual C278 all-token MeanFinalDualReadout for both arms;do not adopt the unsupported
C280 evidence-only mask. This is a training-distribution experiment,not another attention tweak.

## Accepted artifacts

-audit-plan.json:ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2;2603 bytes.
-failure-profile.json:dd80ffb33f3f98aa4b129cef5f5cec56562010b509f5933af41cf76e26d41420;1178793 bytes.
-validation-summary.json:1fc1e6e768b4ebfd1211974fae99dcb35603f2cf06b3e7d54fa7f8479426da2f;15880 bytes.

## Next question, not activation

At identical model capacity and800 updates/model,does alternating two-character and
three-character TRAIN renderings improve both-task reliability over two-character-only
training with the unchanged C278 all-token mean/final dual readout?

Proposed C282 arms:two_char_only and mixed_length,actual identical14256-parameter architecture,
fresh seeds282001..282005,paired identical initial states and logical minibatches,AdamW lr.005,
CE only,no extra training or loss. Mixed-length alternates by epoch so each length has100 full
epochs. Logical TRAIN rows retain200 total exposures;candidate splits those100/100 by length.
Keep C267/C270 datasets/scorers and fixed thresholds,including untouched HOLDOUT value assignments.
Primary candidate PASS requires all5 candidate states to pass both complete tasks.

Critical boundary:three-character names are no longer unseen training lengths or identifiers
for mixed_length. A PASS is seen-length/held-out-value-combination learning only,NOT restoration
of the original unseen-length transfer claim,and NOT a Gate F promotion. Retain two_char_only
as the matched extrapolation baseline. A miss is a valid negative at the fixed budget,not proof
that the architecture can never learn the task.

Separate C282 implementation/preregistration,sealing,committed-byte review and runtime Validate
are required. C282 NOT REGISTERED in this acceptance commit. C283 NOT REGISTERED.
