# C253 acceptance and C254 paired residual-swap boundary

## Formal verdict

**C253 ACCEPTED PASS — diagnostic integrity only.**
C252 remains ACCEPTED VALID NEGATIVE; Gate E PASSED; Gate F NOT PASSED.
No production adoption or model-capability improvement is claimed.

Scientific execution HEAD:13523ebefc482f3b230101d9a89938bda79c69e5.
Published log commit:aca5849d45c9f6c6323db84dc9896a4092144fa0.
Publisher log SHA256:a7690d0e6db2108b4f3e6329e12fbb9a14d8049ba0fbf5ceefc661c02d118880.
Log bytes:655028.
Summary SHA256:2d65feaed637c71728cd8ed1cc60f54306a7fb733b43c6b695e86f0313f27e47.
Local summary:runs/c253-v5b-frozen-residual-97fc39ef6e8b42cba8c2d1933ddfcbf6/summary.json.
Publication is one commit after execution and changes only c253/latest.log/latest.json.
Acceptance uses retrieved immutable log ranges,metadata and recorded user-local postchecks;
no reviewer rerun of accepted checkpoints or independent full-log byte rehash was performed.

## Execution validity

24 own tests PASS in3.166s;3241 focused tests PASS in119.771s.
364 source pins/587 protected inputs. Five frozen models,120 full-model forwards/5760 rows,
zero training,new checkpoint writes0,parent bundle loads1,strict state loads5.
Parent predictions and all metrics including NLL replayed;pre/post/read components unchanged;
restored outputs replayed;weights and protected inputs preserved. Persisted output/component
recomputation PASS. Tracked tree clean;execution HEAD preserved;run_execution_valid=True.

## Deciding outcomes

HOLDOUT exact correct counts per seed,English/Japanese (each language has16 rows):

| Seed | Intact post+read | Pre-core EOS+read | Reader only |
|---:|---:|---:|---:|
|250001|16/16,16/16|15/16,14/16|16/16,16/16|
|250002|9/16,9/16|4/16,3/16|4/16,4/16|
|250003|16/16,16/16|11/16,12/16|10/16,12/16|
|250004|15/16,16/16|10/16,10/16|12/16,12/16|
|250005|16/16,16/16|14/16,14/16|16/16,15/16|

Pooled HOLDOUT:145/160 intact,107/160 pre_residual,117/160 reader_only.
Pooled TRAIN:320/320 intact,225/320 pre_residual,255/320 reader_only.
Pre-residual substitution lowers HOLDOUT accuracy in all10 language cells. Reader-only lowers
7 cells and leaves3 unchanged (250001 EN/JA,250005 EN). No cell improves in either mode.
The previously failed seed250002 is not rescued. Original outputs return after restoration.
All20 intervention/HOLDOUT language NLL deltas are positive. Unchanged argmax in250001 does not
mean unchanged scores:its reader-only HOLDOUT NLL rises from about0.0016 to about0.015.

## Interpretation and limits

The trained post-core residual contributes to accuracy for several models and improves true-answer
NLL in these interventions. It is not uniformly necessary for exact answers:250001 still gets
all original TRAIN/HOLDOUT answers right without it. Reader/core dependence varies with the learned
solution. Current evidence does not support simply deleting or replacing the residual as a repair.

These are frozen combinations of jointly trained features. Removing or replacing a vector changes
activation direction/scale before LayerNorm. A decline does not uniquely establish relation-specific
reasoning,training-time core necessity,or superiority over a separately trained core-free model.
An unchanged score does not establish that the core was unnecessary during learning. No runtime
speed claim is made:the core was still computed in every C253 mode.

## Accepted artifacts

- contrasts.json:e364a74cb9338d7be8c57e85bcbac63e77d169847e83c358175b4e7caaa416d7 (14893 bytes)
- diagnostics.json:5647cbff9a4d214e3c83e77f689e9fde18955c5aef1dba71647c3db9cdd3c6bb (20617 bytes)
- outputs.pt:3e8ba69a46323ed4c47c143f7cacd23ddd42c64cc7a5dbd3973cfd9bff32147c (14140927 bytes)
- residual-plan.json:c48689b9cebedc757261ded1912dbb597884f19ac007d971bcd7bfbfbfd8307d (2115 bytes)
- validation-summary.json:b9cefa29b067961cb9dd181e5ab8be63352b795ee7e91540a63cc2b13d971685 (436 bytes)

## Next question, not registration

Does the post-core residual carry information specific to the recipient's queried entity,or can
a residual from a paired prompt be substituted while the recipient's reader output is fixed?
Use saved C253 intact post/read vectors and the accepted C252 normalization/decoder weights.
Compare self,opposite-fact-order donor (same facts/query),opposite-query donor (same facts/order),
then restored self. Donors remain within the same seed/split/language. Their mapping is a fixed
involution and uses visible prompt metadata,not correctness or a favorable result.

This retains the empirical residual-vector multiset instead of zeroing or replacing it with a
pre-core distribution. It still creates untrained feature combinations and does not identify a
unique semantic mechanism. Recompute only the frozen normalization/decoder;no encoder/core/reader
forward or training is needed. Require intact/restored raw-logit replay and unchanged head weights.
Separate preregistration and committed-byte authoring review control C254 activation.
