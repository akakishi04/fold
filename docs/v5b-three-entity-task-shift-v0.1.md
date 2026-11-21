# V5-B three-entity task shift v0.1 — C256

## One question

Does the C252 aligned reader reproduce its binding/recombination behavior on a fresh three-entity
bilingual assignment task, relative to an equal-parameter EOS-only adapter, using new seeds?

This deliberately ends the two-entity diagnostic chain. C256 does not reuse C252/C255 learned
weights or saved activations. It is a new training/evaluation task under V5-B, not Gate F and not a
general language benchmark.

## Task family

Entities:
- English: a,b,c
- Japanese: 甲,乙,丙

Values: digits0,1,2,3. Each row assigns three distinct values to the three entities.
There are24 possible ordered assignments. A fixed balanced12/12 assignment split is preregistered.
Every entity position sees every value exactly3 times among the12 assignments on EACH side.
Exact assignments never cross the split.

For every assignment:
- English and Japanese;
- canonical and reversed fact order;
- one of three queried entities.

Thus TRAIN144 rows and HOLDOUT144 rows.
Example:
`a=0;b=1;c=2;a=`
and
`甲=0;乙=1;丙=2;甲=`.

Three views:
-normal;
-evidence_blind:all three supplied digits replaced with ?;
-query_blind:queried entity replaced with ?.

The target is exactly the digit assigned to the queried entity. No target,entity ID or answer
position is supplied through any hidden model input. All rendered prompts fit the existing48-slot
byte contract. Dataset SHA256:
`ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b`.

## Models and changed variable

Fresh seeds256001..256005. For each seed create one fresh uncompressed Full V5-B backbone
(13488 parameters), then deep-copy that exact initial state into two arms:

1. aligned_precore_read:
   actual C252 AlignedPrecoreReadout:pre-core EOS query,pre-core K/V token states,learned residual
   read added to the actual post-core EOS state.
2. eos_adapter:
   actual C248 equal-parameter EOS-only16->24->16 residual adapter.

Both add exactly768 parameters;both total14256. Head initialization remains seed+248000 with zero
output projection. Same backbone seed,data,batches,optimizer and budget within each pair.
This is equal parameter count,not equal FLOPs or architecture.

## Training

CPU float64,threads2,deterministic algorithms.
AdamW lr0.005,betas0.9/0.999,eps1e-8,weight_decay0;gradient clip1.
800 updates/model,batch48.

Sampling is fixed and independent of evaluation:
every three steps form one deterministic seed+epoch randperm of all144 TRAIN rows and consume its
three disjoint48-row blocks. Both arms use the same indices for a seed. No HOLDOUT-driven
checkpointing,early stop,seed replacement,extra budget or hyperparameter rescue.

10 models total,8000 updates,384000 training presentations.

## Evaluation and gate

At the fixed final endpoint score TRAIN and HOLDOUT under all three views.

Per language/split:
- normal accuracy;
- answer NLL;
- order_pair_accuracy:both canonical/reversed prompts correct for the same assignment/query;
- query_triplet_accuracy:all three queried-entity variants correct for the same assignment/order;
- evidence/query blind accuracies and drops.

Fixed cell criteria:
- accuracy>=0.90;
- order_pair_accuracy>=0.80;
- query_triplet_accuracy>=0.80;
- evidence_drop>=0.35;
- query_drop>=0.35.

Primary PASS requires every one of the five aligned_precore_read seeds to pass BOTH languages on
BOTH TRAIN and HOLDOUT. The EOS adapter is reported independently and cannot rescue or fail the
primary gate. Individual seed/language cells remain visible;no pooled average can hide a miss.

PASS would establish only bounded task-shift replication on this new authored three-entity family.
FAIL is a valid negative if execution is valid. Neither outcome proves general language skill,
external-dataset generalization,FOLD-core superiority,production adoption or Gate F.

## Replay and workload

After training,serialize10 final states once. Reconstruct each model from its fresh seed and arm,
strict-load the final state,and rerun all6 split/view evaluations.

Per model:
-800 training forwards/38400 rows;
-6 final forwards/864 rows;
-6 checkpoint replay forwards/864 rows.

Total8120 full-model forwards/401280 rows;120 evaluation/replay forwards.
Require changed full/head weights,strict state load,identical saved predictions,metric replay within
1e-9 and raw logits within1e-9. No network calls.

Generated local-only artifacts:
task-plan.json,dataset.json,trained-models.pt,measurements.json,validation-summary.json plus summary.
Judge C256 before C257.
