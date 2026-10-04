# C303 preregistration — residual-gradient routing

Experiment:C303-v5b-residual-gradient-routing. Stage:V5-B-RESIDUAL-GRADIENT-ROUTING.
Acceptance base:d628bf0b901ee6a63fc9e6c5f338fac867e8bcfc.
C302 diagnostic ACCEPTED PASS; C301 ACCEPTED VALID NEGATIVE; Gate F NOT PASSED.
C304 NOT REGISTERED. This is a new learning comparison,not deployment of a C302 swapped condition.

## One question and controls

Does stopping the residual branch's backward signal improve reliable unseen four-character
transfer beyond merely freezing core weights? Keep the original forward sum r+a and train fresh
matched triples. C302 found that final-gain exchanges did not recover the lost quad gate; it did
not identify gradient conflict or show that a branch is defective. This intervention tests that
separate possibility rather than continuing a final-coefficient sweep.

Arms:
- full_train:ordinary full C278 training; no gradient or forward modification;
- core_frozen:keep core parameters at their initial values,but propagate gradients through core
  operations to their inputs normally; this controls for not learning the core;
- residual_stop(candidate):the same frozen core plus stop_gradient(r) at the final sum. The reader
  contribution a remains differentiable. No error signal is propagated from that sum back through r.

All arms compute the original classifier(norm(r+a)). Stop-gradient is an intentional backward
policy,not the true full derivative of the unmodified scalar forward function. Compare its
backward result to an independently detached reference,not finite differences of the full model.
No auxiliary loss,gain,teacher input,output filtering,new tokenizer or extra training examples.

## Exact path,capacity and gradient accounting

Use actual accepted C278 MeanFinalDualReadout inside the new child wrapper. r is the post-core
next-route EOS state. a is the dual-query reader of pre-core local states after read.output.
Capture r before C278's dynamic normalization hook;capture a at read.output;install a late hook
at local_encoder. Require actual norm input exactly r+a on each call. Control hooks return None.
Candidate returns r.detach()+a and verifies exact numerical equality to the original input.
Do not detach a. Keep C278's own provenance checks active and restore hooks even on exceptions.

All states store14256 parameters and use48 tokens,CPUfloat64. The core has3328 parameters.
requires_grad scalar counts:full_train14256,core_frozen10928,residual_stop10928.
The optimizer receives requires_grad parameters only. Core parameters in the two frozen arms
must have no gradients throughout and unchanged final fingerprints. Full-training core must change.
The local encoder is shared by the two paths:core_frozen still sends the residual's error signal
through the fixed core into local inputs;residual_stop does not. Other backbone parameters used
only by r may also receive no gradients in the candidate;do not call all10928 effectively updated.
Record the complete name/numel/trainable/core inventory,per-update gradient-receiving scalar count,
per-update core gradient count,and union of gradient-receiving parameter names. None gradients are
not numeric zeros. These measurements do not establish equal backward compute or runtime.

Require initial state equality across each triple,independent parameter storage and exact initial
logits/first CE. Reader-parameter gradients at the first update must match across arms;core/input
parameter gradients deliberately differ. The operational probe also compares the unwrapped original.
Gradient norms and global clipping may change with the policy;that is part of the intervention.
Freezing core does NOT freeze its activation:it still depends on changing shared local inputs.
All forward core/reader computations remain;there is no inference speed or core-removal claim.

## Fixed learning and evaluation

Fresh initial seeds303001..303005,order seeds303101..303105 paired in order. All three arms of a
seed use identical initial numerical weights,examples/order and private shuffle. No old trained
or recombined model weights are used. Global fit RNG606000 resets before every fit.
Ordinary mean CE;AdamW lr.005,betas(.9,.999),eps1e-8,weight_decay0,clip1,one optimizer800updates.
200epochs*4updates;randperm96(generator order+303000+epoch);24intact pairs/48rows per update;
length=epoch%2,profile=epoch%3. Each logical row is used100 times at each trained length.
Only normal two/three-character TRAIN is optimized. HOLDOUT/quad/masked inputs are evaluation-only.

Freeze all final parameters,score two/three/quad with original normal/evidence-blind/query-blind
views,and strict-load/replay all15 states. During inference stop-gradient changes no numeric value.
Original thresholds stay accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Primary candidate PASS iff all5 residual_stop states pass every original quad criterion. Report
both controls separately;absolute PASS is not automatic superiority or Gate F completion.
Report15 seed/arm results,90 final partitions,60 candidate-versus-control correct-count contrasts,
TRAIN/HOLDOUT direct flags,core change flag and measured gradient-receiving capacity.
No successful-cell selection,checkpoint selection,gradient-policy sweep or threshold change.

## Exact parent contract and protection

C302 execution:cfb1092c859f9e5512dcfdd63858973ab2194710.
Publication:4ce7a79c904dac84c6916825d1d801d202580665.
Summary:runs/c302-v5b-gain-cross-d81285be58684cbfbb6d3ec7253a42ca/summary.json.
SHA256:1054849a7c416eb0a32f53e114df5501401b3f4acfeec1f6dc5aa4276d302b10.
Source:model_c302_frozen_gain_cross.py;Git blob1eb77daeb4fd53141ad31a6ad3c60ceba9ce3ad2.
C278 readout blob0aa8d65874f4a021e21d04948ffd0a1d5615248b remains pinned.

Verify29 ordered hashes BEFORE exact C302.verify_artifacts with28 ancestor summaries and its
accepted execution HEAD. Tail hashes are C302.PARENT_SHA and C301.parent_hashes(C300). Require
PASS,all weights/hooks preserved,diagnostic-only status and the actual2x2 task counts from C302.
The exact summary seals its four artifact descriptors. C302 has no dataset or trained-model
checkpoint;read recursively verified C301 dataset/triple/quad JSONs at the next ancestor path,
and recheck canonical hashes from immutable C299 through C301/C300 contexts.

Only direct import is C302. Its context provides C301 plus inherited audit,normalizer,evaluator,
quad scorer,table builder and model/core modules. Use C301.counted on the new wrapper and the
C296 pair/render helpers through C301.pair_source(C300);do not call old cohort-specific analyzers
with C303 seeds/arms. All reachable helpers remain in the inherited658-source/1217-input maps.
Check actual repository-local context and pair-helper coverage. Add OWN6 plus5 C302 files:
source664/protected1228. Do not modify accepted sources,tests,logs or dispatchers.

## Workload,persistence and review boundary

15new models*800=12000updates;576000training rows. Each model800training+81scoring+81replay
forwards=962. Total14430forwards,809280row presentations,57720core calls. One15-state bundle
write/read,15strict state loads,network0. Backward compute differs and is not estimated by these
forward counts. Operational probe4forwards/backwards,regression and old-artifact checks are separate.
Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json.
Schemas:fold-c303-gradient-models-v1 and fold-c303-gradient-eval-v1. Save every800-step loss,
gradient count,parameter inventory/schedule,initial/final/core fingerprints and final raw logits.
Full datasets/tensors/maps stay local/ignored;mirror only compact console receipts and aggregates.
The saved verifier recomputes schedules,gates,comparison tables and all invariants without forwards.

Own40/modules188/loaded4710/focused4709;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:265067d9ca156f5181b6275ce4274ffee919751bcf1cd395b470656bce163ad7.
Commit/re-fetch/post-authoring review of OWN6 is mandatory before activation/command release.
Test explicitUTF8/CP932,free names,runner indexes,gradient policy,actual C278 class integration,
loader/call ordering/counts and persistence. Synthetic tests are not actual FOLD results.
Mandatory Windows Validate checks29parent archives,664/1228pins,real initial logits/gradient
routing,own40 and full4709. Preserve dispatcher/selected-launcher/runner ParseFile chain.
Validate failure skips science/publication;integrity failure repairs SAME C303 without changing
conditions. Valid all-five miss is ACCEPTED VALID NEGATIVE. C304 waits for formal C303 judgment.
