# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold; branch:feat/sft-target-loss; local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 via explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 stays immutable/pinned.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; Gate E PASSED; Gate F NOT PASSED.
**C302 ACCEPTED PASS (diagnostic integrity only). C303 ACTIVE / NOT YET JUDGED. C304 NOT REGISTERED.**
C301 remains ACCEPTED VALID NEGATIVE. C303 is the unique ACTIVE residual-gradient comparison.
Latest accepted scientific execution:cfb1092c859f9e5512dcfdd63858973ab2194710.
Latest accepted published log:4ce7a79c904dac84c6916825d1d801d202580665. Do not rerun C302.

## Latest accepted evidence — C302

Acceptance:docs/experiment-ledger-addendum-c302-c303.md.
Acceptance commit:d628bf0b901ee6a63fc9e6c5f338fac867e8bcfc.
Summary:runs/c302-v5b-gain-cross-d81285be58684cbfbb6d3ec7253a42ca/summary.json.
SHA256:1054849a7c416eb0a32f53e114df5501401b3f4acfeec1f6dc5aa4276d302b10.
Own32/focused4669 PASS; source658/protected1217; run_execution_valid=True.
All10 baseline/restoration comparisons have zero logit drift;all weights/hooks preserved.
Fixed weights have quad2/5 at unit and trained gains;learned weights have quad1/5 at either.
Learned-weight seen gates are two3/5 at either gain;triple2/5 at unit and3/5 at trained gain.
301003's missing quad HOLDOUT answer is not recovered by returning the gain to1.
301005 HOLDOUT correct(two/triple/quad;denominator288):
fixed/unit278/273/262;fixed/trained279/274/266;learned/unit288/287/279;learned/trained288/288/283.
Weight-state differences persist at equal gain,and some immediate gain effects remain too.
Do not confuse unchanged gate counts with unchanged individual predictions or assign additive
unique causal shares. C301 remains negative;no coefficient sweep or inference substitution adopted.

## Active C303 — residual-gradient routing

Experiment:C303-v5b-residual-gradient-routing. Stage:V5-B-RESIDUAL-GRADIENT-ROUTING.
Registration:docs/experiment-ledger-addendum-c303-preregistration.md.
Design:docs/v5b-residual-gradient-v0.1.md.
Review:docs/c303-post-authoring-review.md.
Acceptance base:d628bf0b901ee6a63fc9e6c5f338fac867e8bcfc.
Authoring/review target:2974cc1af29b5a264642cc57d7c74f04e99b1281.

One question:does stopping the residual branch's backward signal improve reliable untrained
four-character transfer beyond merely freezing core weights? Fresh matched triples:
-full_train:original full training;
-core_frozen:freeze core parameters at initialization,but propagate through core to its inputs;
-residual_stop(candidate):same frozen core plus stop_gradient(r) at the final residual/reader sum.
All numerically compute classifier(norm(r+a));no gain,branch deletion or inference-time selection.
A sole stop-gradient comparison would confound core freezing with altered shared-input gradients;
the middle control separates those interventions. Global clipping/optimization may still differ.
This is a new hypothesis,not proof that C302 discovered a gradient-conflict mechanism.

r is the post-core next-route EOS state;a is the additional reader output from pre-core local
states. Actual unchanged C278 class is wrapped. Temporary hooks capture r and a and append the
candidate hook after C278's own dynamically registered sum. Require exact actual norm input r+a
on every call. Controls leave it untouched;candidate r.detach()+a must have the same numeric value.
Do not detach the reader contribution. Original assertions stay active;all hook registries restore
on success/failure. Core and reader forwards remain,so no inference-speed/core-removal claim.

Each model stores14256 parameters;core3328. requires_grad counts are14256/10928/10928 by arm.
AdamW includes only requires_grad parameters. Frozen cores must have no gradients and unchanged
final fingerprints;full-training core must change. Shared local features continue learning through
the reader. Freezing core parameters does not freeze their input-dependent activations. Other
r-only parameters may receive no gradient in the candidate:measure,do not claim all10928 update.
Save complete parameter inventory,each update's gradient-receiving scalar/core counts and union
of parameter names. None is not a numeric zero. Backward cost and active-learning capacity differ.

Fresh initial seeds303001..303005,order seeds303101..303105 paired in order. All arms use identical
numerical initial common weights and input order within seed,independent storage,fitRNG606000.
Require first-step logits,CE and reader gradients to match;core/input gradients intentionally differ.
Initial real-data preflight also compares plain C278 to wrappers. Reader gradient equality is
pre-clipping,not equality of later parameter trajectories. No previous trained/recombined weights.

Ordinary mean CE;one AdamW800steps,lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1.
200epochs*4updates;96intact pairs,24pairs/48rows per update;private shuffle order+303000+epoch;
length=epoch%2,profile=epoch%3;each logical row100 exposures at each trained length.
Only normal two/three-character TRAIN is optimized. No HOLDOUT,quad,masked or teacher-input leakage.

Freeze final models;score unchanged two/three/quad normal/evidence-blind/query-blind tasks and
strict-load/replay all15 saved states. Inference stop-gradient changes no numerical value.
Primary PASS iff all5 residual_stop states pass every original quad criterion. Gates unchanged:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Both controls are reported.
Absolute PASS is not automatic superiority,production adoption or Gate F completion.
Report15 results,90 final partitions,60 candidate-versus-control correct-count contrasts,
TRAIN/HOLDOUT direct flags,core-change flags and measured gradient-receiving parameter totals.
No checkpoint/seed/policy selection after seeing outcomes.

## Parent contract,protection and workload

Verify29 ordered hashes BEFORE exact C302.verify_artifacts(parent_dir,28 ancestors,accepted HEAD).
C302's exact summary seals4 diagnostic artifacts;it has no dataset or trained checkpoint copies.
Require diagnostic PASS,preserved weights/hooks and exact2x2 counts. Read recursively verified
C301 dataset/triple/quad at the next ancestor path and recheck canonical hashes via immutable
C301->C300->C299 contexts. No C302 archive is used as a model initializer.
Sole direct import C302. Its context exposes C301 and inherited audit/normalizer/evaluator/quad/
tables/core modules. C301.counted handles the new wrapper;C301.pair_source(C300) yields C296
pair/render helpers. These actual context/helper modules must be source-pinned. Do not use old
cohort validators with new identities. Retain658source/1217input maps;OWN6+5 C302files=>664/1228.
C278 readout blob0aa8d65874f4a021e21d04948ffd0a1d5615248b stays pinned. No accepted file edits.

Science:15models,12000updates,576000training rows,14430forwards,809280total row presentations,
57720core calls,15strict state loads,one15-state checkpoint bundle write/read,network0.
Forward counts do not measure the different backward work. Operational real probe4forwards/
backwards,regression and recursive parent checks are separate from science.
Eight outputs plus summary:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json.
Schemas:fold-c303-gradient-models-v1 and fold-c303-gradient-eval-v1. All state keys use model.*;
correct arm factory reconstructs requires_grad policy,then replay freezes every parameter.
Persist all800 losses/events/gradient counts,parameter inventories and raw final predictions.
Full datasets/tensors/maps stay local/ignored;only compact console receipts/aggregates are mirrored.
Own40/modules188/loaded4710/focused4709;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:265067d9ca156f5181b6275ce4274ffee919751bcf1cd395b470656bce163ad7.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static review and executed local behavioral tests).
All6 OWN files re-fetched at2974cc1af29b5a264642cc57d7c74f04e99b1281;whole-file blobs match6/6.
After all matches:normal own40 PASS in9.077s;entire CP932-emulated own40 PASS in10.217s.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5;both Python files/3embeddedblocks compile;
free-name audit0,UTF8/noNUL,manifest matches. Tests execute800updates per arm on controlled toy
models,verify detached-reference gradients,distinguish frozen-core from stopped-residual input
gradients,and check original/three-arm initial logits/reader gradients and exception cleanup.
Actual accepted C278 class AST integration uses substitute backbone/reader components. Its local
support file is a fetched class slice and is not committed;Windows reads the full accepted module.
Toy inputs/padding are software controls,not FOLD evidence. Parent archives,Git/scorers and suite
members are substituted where unavailable. Production-path ordering/bundle/replay/persistence,
29hash guards,664/1228protection,semantic test IDs and UTF8 checks passed in that bounded scope.
Real Windows29-parent validation,protected bytes,PowerShell ParseFile,actual initial gradient
checks,the real4709 inherited regressions,and15 actual FOLD fits/replays remain mandatory gates.
Activation must preserve all6 reviewed OWN blobs and every accepted file/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 via explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C303 -> Validate(29parents,664/1228
protection,real initial logits/gradient-route checks,own40,focused4709) ->
authoring_runtime_preflight=PASS -> Execute(15models*800updates,frozen original scoring,
strict state replay,gradient/capacity accounting,persisted reconstruction) -> log publication.
Validate failure skips science/publication. Integrity failure repairs SAME C303 with fixed conditions.
A valid all-five miss is ACCEPTED VALID NEGATIVE. Do not change cohort,gradient policy,LR,budget
or thresholds after results. C304 is unregistered until C303 formal judgment;Gate F NOT PASSED.
Separate scientific execution HEAD from the later publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full previous handoff:docs/handoff-history/c302-pre-acceptance.md.
Git blob:6cc34252167ace2e9ae7dab831f16ac130a9e860. Accepted files stay immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
