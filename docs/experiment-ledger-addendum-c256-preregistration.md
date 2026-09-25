# C256 preregistration — fresh three-entity task shift

Experiment:C256-v5b-three-entity-task-shift.
Stage:V5-B-THREE-ENTITY-TASK-SHIFT.
C255 ACCEPTED PASS (diagnostic integrity only). C257 NOT REGISTERED.
Gate E PASSED;Gate F NOT PASSED.

## Question

Does the C252 aligned pre-core reader reproduce its bounded binding/recombination behavior on a
fresh three-entity bilingual assignment task with new seeds,relative to an equal-parameter
EOS-only residual adapter?

This is a new training task,not a frozen diagnostic and not an attempt to rescue any C252 seed.

## Accepted parent identity

Acceptance/base commit:0455a2aed54c54fd1dbc6008cf6f7b80f0521aae.
Acceptance record:docs/experiment-ledger-addendum-c255-c256.md.
C255 scientific execution HEAD:6b577da1edc7339dbfd68b3127870074de218e48.
Published log commit:48856dd7dabb84f1f8a71158d03a5ee9db2fd255.
Publisher log SHA256:a733f750125ccacfc5ce54867bce122c91561bd105e9d1eac1adaf04ab13bc2d.
Parent summary SHA256:6c4e9a569a7c622259b501f209781b357d183dfbaf5750a6d6c939f5e59e3150.
Parent path:runs/c255-v5b-value-residual-8203653a07964d9bb549c272a8b9b943/summary.json.

Required C255 artifact identities:
-contrasts.json:ecc69baf18f5824ad3c94be836ba55b2f05ace64f5b38d42825dbce37c48f228
-diagnostics.json:111b4c2d98087f0d7e90cddda83ba53892eb74961cb4b0a564392eb36ccc51a4
-head-outputs.pt:77a4e8a54e610a40cd7be3965e863d48e4f5058efebbc49637aa40d043cf1241
-validation-summary.json:69394982329cd77f7ae0d9739f7fe97e898444e331b697fa507287120be99b63
-value-plan.json:e5a6589105d534218c9056768c2af3e60da136a2dfb9f9fa8393bba9198a548a

C255 must validate as diagnostic PASS. Its two earlier invalid attempts remain recovery evidence only.

## Fixed task and split

Entities EN:a,b,c;JA:甲,乙,丙. Values0..3. Three distinct values per assignment.
All24 ordered assignments are partitioned into fixed12 TRAIN and12 HOLDOUT assignments.
Each entity-position/value marginal equals3/12 on each side. Exact assignments do not overlap.

For every assignment create2 languages x2 fact orders x3 queries=12 rows:
TRAIN144,HOLDOUT144. Normal/evidence_blind/query_blind views.
Target is the one digit bound to the queried entity.
Task SHA256:ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b.
No future byte,target ID,entity index or answer location is given to the model.
All prompts satisfy the existing BOS+bytes+EOS+PAD48-slot contract.

## Arms and initialization

Seeds256001..256005,never used by C250-C255.
For each seed instantiate actual fresh Full backbone through the protected C231 factory,record its
state fingerprint,and deep-copy that exact state to both arms.

aligned_precore_read:
actual C252.AlignedPrecoreReadout. Pre-core EOS query and pre-core K/V memory;reader output added to
actual post-core EOS before the original LayerNorm/decoder.

eos_adapter:
actual C248.ReadoutPilot family=full arm=eos_adapter. Equal768 added parameters;post-core EOS-only
residual MLP.

Both14256 parameters. Both original output projections initialize to zero through seed+248000.
No accepted checkpoint initializes either arm. C255/C254 activations never enter C256.

## Fixed training

800 updates/model,batch48,10 models.
AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0;clip1.
CPU float64,threads2,deterministic algorithms.

For step s:epoch=floor(s/3),block=s mod3.
Generate one randperm(144) from CPU seed+256000+epoch and use its block of48.
Thus every complete3-step epoch covers all TRAIN rows exactly once;both arms use identical batches.
No HOLDOUT input enters optimization. No early stopping,seed replacement,checkpoint selection,
extra steps or post-result threshold change.

## Fixed metrics and gate

Score final TRAIN/HOLDOUT,normal/evidence_blind/query_blind.

Each language has72 rows/split.
order_pair groups same assignment/query across the2 fact orders:36 groups/language.
query_triplet groups same assignment/order across all3 queries:24 groups/language.

Per-cell PASS:
-normal accuracy>=0.90;
-order_pair_accuracy>=0.80;
-query_triplet_accuracy>=0.80;
-evidence_drop>=0.35;
-query_drop>=0.35.

Primary C256 PASS iff all five aligned_precore_read seeds pass both languages on both TRAIN and
HOLDOUT. The EOS adapter is an independent equal-parameter control and never rescues primary status.
A complete valid miss is ACCEPTED VALID NEGATIVE.

Report per seed/arm/split/language metrics,seed pass counts,cell outcome categories and10 paired
candidate-minus-control HOLDOUT accuracy comparisons.

## Workload and replay

10 models x800=8000 training updates/384000 presentations.
Per model806 forwards/39264 rows through training+final scoring,then6/864 strict checkpoint replay.
Total8120 full-model forwards/401280 rows.
Evaluation+replay forwards120. One10-state checkpoint bundle;new checkpoint writes1.
No network calls.

Require:
-common backbone identity before both arms;
-total/head weights change;
-strict state load;
-final-state fingerprint replay;
-saved prediction identity;
-all final metrics replay within1e-9;
-raw logits replay within1e-9;
-source/artifact/task hash preservation.

## Source protection and authoring contract

Inherit C255376 source pins/611 protected inputs.
Add parent summary+five artifacts and OWN6 ->382 source pins/623 protected inputs.
Explicit deciding-path dependency union32=five C231 LM_SOURCES plus C230..C256 benchmark/helper
entry modules. All lazy imports on the scientific path are included.

OWN6:
-fold_lm/v05_benchmarks/model_c256_three_entity_task_shift.py
-tests_lm/test_v05_c256_three_entity_task_shift.py
-tools/run_c256.ps1
-tools/invoke_c256.ps1
-this preregistration
-docs/v5b-three-entity-task-shift-v0.1.md

Own tests24;modules141;loaded3314/focused3313.
Only inherited exact historical exclusion:
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.

Artifacts5:task-plan.json,dataset.json,trained-models.pt,measurements.json,validation-summary.json.
Bundle schema fold-c256-three-entity-v1.
Manifest SHA256:31b433a189aee26a02d11d1571300b216f21ceb205d3696f90fe95d02bb20a7c.

## Interpretation boundary

C256 is a task-family shift within authored symbolic assignment tasks. PASS does not establish a
general benchmark result,conversational language capability,external generalization,core
superiority,production adoption or Gate F. The EOS adapter is parameter-matched but not compute-
or architecture-matched. FAIL does not erase C252's bounded4/5 result.

After all six OWN files are committed,re-fetch committed bytes,compile/import,run exact own tests
where possible,and audit free names,task hash,sampling,metrics,pair definitions,parent source
protection,counts,CLI indices and PowerShell parser ordering. Do not issue a launcher before
post-authoring review PASS is recorded in the handoff.

Judge C256 before C257.
