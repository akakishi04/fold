# C301 preregistration — learned global residual gain

Experiment:C301-v5b-learned-residual-gain. Stage:V5-B-LEARNED-RESIDUAL-GAIN.
Acceptance base:32bbfd3e74a0031ae8c327c7426d5a2900bd5c5e.
C300 ACCEPTED PASS (diagnostic integrity only). Gate F NOT PASSED. C302 NOT REGISTERED.

## One question

Does a global residual gain learned only from TRAIN improve reliable unseen four-character transfer
against the original fixed gain1 at the same800-update budget? C300's reader-only inference rescued
one quad gate but lost one seen-length gate and caused large regressions elsewhere. That does not
justify discarding a branch or establish the cause of learning failure. This is a new learning
hypothesis with fresh paired models,not deployment of C300's best branch or failed-seed tuning.

## Exact intervention and matched initial function

Use the actual accepted C278 MeanFinalDualReadout inside a new wrapper. The original model's
pre-normalization sum is r+a,where r is post-core next-route EOS residual and a is the output of
the additional dual-query memory reader. The original classifier and normalization are retained.
Control fixed_gain leaves this exact sum unmodified. Candidate learned_gain passes alpha*r+a,
alpha=2*sigmoid(g),with one scalar g initialized exactly0,so alpha is exactly1 at initialization.
The mathematical range is0<alpha<2;float64 may reach endpoints through saturation,which is recorded
and not silently clipped or rejected. No sign reversal. The same alpha is used for every example,
length,language and mask within a model. It is frozen after training,not selected from evaluation.

Temporary instance hooks capture the original r and a WITHOUT detach or clone-to-detach. Require
actual C278 normalizer input exactly equals r+a before substituting alpha*r+a. Capture order,
batch-by16 CPUfloat64 finite tensors,single formula check and hook restoration fail closed.
Existing C278 assertions and its forward remain intact. The original dynamically registered norm
hook is followed by the candidate hook,installed during local_encoder. Gradients flow through
both terms and g. The control late hook returns None. No accepted source is edited or monkeypatched.

Common model parameters match within each seed. Compare exact first-input logits/CE and gradients
of every original parameter BEFORE clipping,including None gradients. A mandatory real-data runtime
preflight compares plain C278,wrapped fixed control and initial learned candidate. Synthetic finite
 differences and the actual accepted C278 class AST integration test check differentiability.
The shared initial function does not imply later common weights remain equal. Candidate g participates
in the same global gradient norm clipping and AdamW update;this is part of the policy,not controlled away.

## Cohort and held-constant learning

Fresh initial seeds301001..301005 paired with order seeds301101..301105 in order. Both arms use
the same corresponding initial state and example schedule;no C299 learned or recombined weights.
Remaining global Torch fit RNG602000 is reset for every fit. All10 models are independently stored.
Original C278 parameters14256;candidate14257 including exactly one new learned scalar. No padded
control parameter and no false equal-capacity claim. Width16,48-token context,CPUfloat64,2threads.
All original parameters remain trainable. All upstream computation,including4 core calls/forward,
still executes. No inference-time routing,filtering,core removal,auxiliary loss or speed claim.

Ordinary mean CE;one AdamW800 steps,lr.005,betas(.9,.999),eps1e-8,weight_decay0,global clip1.
200epochs*4 updates;24 intact TRAIN query pairs/48 rows per update. Private shuffle Generator
order_seed+301000+epoch;length=epoch%2,profile=epoch%3. Each logical row100 exposures at each trained
length. Two/three-character normal TRAIN only. HOLDOUT,quad and masked views never optimize g or
other parameters. Four-character TRAIN-value split is not trained four-character input.

## Fixed gate and reporting

Freeze final models,including g;evaluate all old two/three/quad normal,evidence-blind and query-blind
views with unchanged thresholds:accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80.
Primary candidate PASS iff all5 learned_gain states pass every original quad criterion. Report all
control outcomes separately. Absolute PASS does not establish superiority over the control or Gate F.
Ten cell results,60 task/split partitions,30 paired accuracy-count comparisons. Report fitted-TRAIN
and seen-HOLDOUT direct flags and each model's final gain. Save all800 CE/pre-update g/alpha values,
final g/alpha,actual schedules and initial common gradient fingerprints. Do not select a checkpoint,
best coefficient,successful seed or per-question mode after seeing evaluation. A coefficient learned
on TRAIN need not be optimal for HOLDOUT;no success guarantee or isolated causal claim.

## Exact parent writer/loader boundary

C300 execution:b1d24f9ca330711802eb450f86fc3b4c64d88666.
Publication:14e8a6972c0364a30ddb755c5d45d678d5673bea.
Summary:runs/c300-v5b-readout-terms-ba7889d232f342d591bb8b75f48cb853/summary.json.
Summary SHA256:440d5dcd9b8293f3925f394fa9ea1fc08d9754dfd67fc411340c5d6d1548fed3.
Parent source:model_c300_frozen_readout_terms.py;Git blob7299772d37af3a6b693a922ca63d2418565f2d69.
C278 readout blob0aa8d65874f4a021e21d04948ffd0a1d5615248b is explicitly retained.
Verify27 ordered summary hashes BEFORE dispatch:C300,C299,...,C274. Tail hashes come from immutable
C300/C299 constants. Call exact C300.verify_artifacts with26 ancestor paths and accepted execution
HEAD;validate its four artifacts,original before/after matrices,weights/hooks and diagnostic flags.
C300 has NO dataset copies or model checkpoint. After recursive verification,read C299's already
verified dataset/triple/quad files and recheck their canonical hashes. No C300 archive is treated
as a trained-model bundle or as a learning dataset. No old trained state is loaded for new training.

Sole direct repository import C300. Its context exposes C299 and inherited C294 no-neural,C287
normalizer,C284 evaluation/replay_error,C283 quad,C282 tables and core bundle. C296 pair/render
helpers come through C299.context()[2];their exact current source is inherited/pinned. The C301
writer has seed/arm identities,new wrapper-prefixed state keys and an optional gain_logit entry.
Its own strict-load replay uses the correct wrapper and checks final gain plus full fingerprint.
Do not use an old cohort validator or assume all records have14256 parameters. Entire source map
646 and input map1191 remain protected;add OWN6 plus C300's5 files:source652/protected1202.

## Workload and artifacts

10 models*800=8000 updates;384000 training rows. Each800 training+81 evaluation+81 strict replay
forwards=962. Totals9620 forwards,539520 presentations,38480 core calls. One10-state bundle write/
load,10 model-state loads,new checkpoint1,network0. Parameter copies and scalar sigmoid arithmetic
are not extra model forwards. Operational preflight includes3 real forwards/backwards and is
separate from science. All phase costs remain in logs;no wall-clock or memory improvement claim.

Outputs:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,trained-models.pt,
evaluations.pt,measurements.json,validation-summary.json,plus summary.json. Model schema
fold-c301-gain-models-v1;eval schema fold-c301-gain-eval-v1. Exact output hashes/sizes,final gain,
raw logits,answer argmax and replay drift<=1e-9 are verified. Numerical persisted reconstruction
rebuilds schedules,gain histories,gates and comparisons without neural calls. Full tensors/maps
stay local/ignored;compact receipt and aggregates only in the mirrored console log.

Own40/modules186/loaded4638/focused4637;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:c10f5dd5be005595a12502ff9ebe43802f987464ca1b85da2adb28a47f175dd9.
Commit/re-fetch and independently review OWN6 before activation/command release. Require explicit
UTF-8 reads,CP932-emulated whole-suite checks,actual run-path loader/count/order tests,free-name
binding audit,manifest,CLI indices and unchanged accepted files. Windows Validate verifies27 real
parents,pins,real initial function/gradient identity,own40 and full4637 tests. Preserve dispatcher/
launcher/runner ParseFile chain. Validate failure skips science/publication. Invalid integrity
retries SAME C301 with fixed conditions. Valid all-five miss is ACCEPTED VALID NEGATIVE.
C302 stays unregistered until C301 formal judgment;Gate F does not change automatically.
