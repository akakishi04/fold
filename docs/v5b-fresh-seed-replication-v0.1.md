# V5-B paired fresh-seed replication v0.1 — C250

## Question

Does the unchanged C248 reader-versus-EOS-adapter recipe reproduce its bounded TRAIN/HOLDOUT
performance in five prospectively fixed new initialization blocks?
C248 produced promising individual reader cells but failed its all-seed criterion. C249 showed
that those frozen readers depend on their added residual and learned weighting. Neither result
establishes repeatability across fresh initial conditions. Before further model changes, keep the
recipe fixed and measure this new batch without replacing failed seeds.

## Fixed experiment and changed seeds

Use seeds250001,250002,250003,250004,250005. Every seed includes Full/GRU-only and token_read/
eos_adapter:20 models. The head rule remains seed+248000, not seed+250000. The original backbone
and head initializations thus change together; this does not isolate which causes a seed effect.
These five blocks are the unit for reporting initialization repeatability. Languages and arms
within a block are correlated comparisons, not extra independent training replicates.

Reuse actual C248.ReadoutPilot,ResidualHead,train_one and fit without edits or monkeypatches.
Both arms add768 parameters:Full14256,GRU-only10928. Architecture, zero output-projection start,
all-nonPAD token eligibility, width16,48 slots,byte input and256-class output remain unchanged.
Use C244's old32/added32 alternating normal-input schedule,400 updates/model,batch32,AdamW
lr0.005,betas(0.9,0.999),eps1e-8,weight_decay0,clip1,CPU float64,threads2,deterministic algorithms.
No erasure augmentation, additional loss, layer change, early stopping or best-checkpoint choice.
A console-only stream adapter relabels inherited [C248] progress as [C250];it does not edit code.

The TRAIN64/HOLDOUT32 partition is byte-identical to C248. No accepted trained checkpoint is loaded
as initialization. The task and held-out prompts have been repeatedly examined in this adaptive
research series:these are new initializations,not a pristine external evaluation dataset.

## Fresh references and equal starting points

Old-seed fingerprints cannot be imposed on new seeds. For each new seed,construct the Full backbone
and its common-weight GRU-only copy before either arm trains. Evaluate each family backbone once,
on the three original TRAIN views only,recording its before-training fingerprint and metrics.
Copy that unmodified backbone separately into both arms;C248.train_one requires the fresh backbone
fingerprint and initial metric replay. Verify that fitting an arm never changes the shared source.
The original reference state is not a learned checkpoint and no HOLDOUT row enters this reference
calculation. All scientific reference forward costs are counted.

Each model is trained once to400 updates,then final TRAIN/HOLDOUT evaluation and strict checkpoint
replay are performed. Failed TRAIN/HOLDOUT criteria are valid observations;do not change the seed
list,reset a model,extend training or select the better of repeated runs. Existing C248 results,
including seed234002,remain visible and unchanged.

## Gates and reports

Retain original per-language criteria on BOTH TRAIN and HOLDOUT:
accuracy>=0.90;fact/query/order paired both-correct>=0.80;both mask drops>=0.35.
TRAIN32 questions/language requires29/32 and13/16 pairs;HOLDOUT16 requires15/16 and7/8 pairs.
Primary status is PASS only when every new Full/token_read seed passes both languages/splits.
Report independent family/arm gates,all per-seed metrics,reader-minus-control paired differences,
and the number of whole seed blocks passing both languages for each family/arm (out of5).
Do not turn20 reader language cells into20 independent replicates or pool away a failed seed.

A primary miss is ACCEPTED VALID NEGATIVE for this fixed new batch. A primary pass concerns only
this batch and task. It does not erase C248's negative,guarantee a population success probability,
prove general language or justify Gate F/production adoption. If the equal-parameter EOS control
also succeeds,the result does not establish a reader-specific advantage. Parameters are matched;
compute and optimization geometry are not. No statistical significance claim is preregistered.

## Exact accounting and integrity

20x400=8000 training updates/256000 answer presentations.
Per trained model:C248's409 forwards/13280 rows before reload plus C244's6/288 replay gives415/13568.
For20 models:8300 forwards/271360 rows. New references add10 backbones x3 TRAIN forwards/192 rows:
30 forwards/1920 rows. Grand total8330 full-model forwards/273280 presented rows.
There are330 evaluation forwards in total,including fresh references. One new20-state bundle.
No parent inference or scientific network calls. Authoring synthetic tests are separate work.

Preserve every source/input hash,reference identity,model capacity,schedule,head/whole-model weight
change and initial/reloaded prediction/metric replay. Postcheck reconstructs discrete final metrics
and validates the stored fresh references without additional model forwards. C250 has six local
artifacts because initial-references.json is retained separately. No old parent summarizer or
12-state loader is used for new20-model records.

Any source,artifact,schema,nonfinite,replay,mutation,count or test fault is INVALID / RETRY SAME C250.
Preserve accepted sources/tests/logs. Numeric-memory and erasure-mixture tuning remain paused.
No new production architecture,paid API,external corpus,cleanup or history rewrite. Judge C250 before C251.
