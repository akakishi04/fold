# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md response format v2.
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
Entry:tools/invoke_active_v2.ps1 through explicit PowerShell7 and dispatcher ParseFile.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.
**C300 ACCEPTED PASS (diagnostic integrity only). C301 ACTIVE / NOT YET JUDGED. C302 NOT REGISTERED.**
C299 remains diagnostic PASS;earlier capability negatives remain unchanged.
C301 is the unique ACTIVE learned-global-residual-gain comparison.
Latest accepted scientific execution:b1d24f9ca330711802eb450f86fc3b4c64d88666.
Latest accepted published log:14e8a6972c0364a30ddb755c5d45d678d5673bea. Do not rerun C300.

## Latest accepted evidence — C300

Acceptance:docs/experiment-ledger-addendum-c300-c301.md.
Acceptance commit:32bbfd3e74a0031ae8c327c7426d5a2900bd5c5e.
Summary:runs/c300-v5b-readout-terms-ba7889d232f342d591bb8b75f48cb853/summary.json.
Summary SHA256:440d5dcd9b8293f3925f394fa9ea1fc08d9754dfd67fc411340c5d6d1548fed3.
Own40/focused4597 PASS;source646/protected1191;run_execution_valid=True.
Manifest:31d1418e00e6a26cd5f541f47353bf3d947e4feebf0c807a87e8b7e069ef2e30.
All9 original states/logits reproduce before/after intervention with maximum drift0.0;weights and
hooks unchanged. Science training0,2916forwards,279936rows,11664core calls,9state loads,0new checkpoints.
Full seen tasks7/9 and quad3/9. Residual-only0/9 throughout. Reader-only seen tasks6/9 and quad4/9.
Reader-only remaining297002/core297002 rescues2 quad HOLDOUT answers286->288 and passes quad.
Remaining297002/core297003 loses1 HOLDOUT answer at each seen length and4 quad HOLDOUT answers.
Remaining297001/core297003 quad TRAIN553->357 (14rescues,210regressions);HOLDOUT159->121.
No unconditional ablation adoption. All upstream computation still executed;inference ablation
and normalization changes do not prove a training cause or core dispensability.

## Active C301 — TRAIN-learned global residual gain

Experiment:C301-v5b-learned-residual-gain. Stage:V5-B-LEARNED-RESIDUAL-GAIN.
Registration:docs/experiment-ledger-addendum-c301-preregistration.md.
Design:docs/v5b-learned-residual-gain-v0.1.md.
Review:docs/c301-post-authoring-review.md.
Acceptance base:32bbfd3e74a0031ae8c327c7426d5a2900bd5c5e.
Authoring/review target:36156946c5035ba6f52e5973d0f5f9e2ded9898b.

One question:does learning a global residual gain from TRAIN improve reliable unseen four-character
transfer versus fixed original gain1 at the same800-update budget? Fresh paired initial seeds
301001..301005 with order seeds301101..301105. Each pair has identical original initial parameters,
examples and order,independent storage. No C299 learned/composed states reused for initialization.

Control fixed_gain preserves actual C278 normalizer input r+a unmodified. Candidate learned_gain
uses alpha*r+a,alpha=2*sigmoid(g),one scalar g initialized0 and alpha exactly1. r is the post-core
next-route EOS residual;a is the additional dual-query memory-reader output,not the classifier.
Same alpha for every input/length/language/mask within a model;learned only on TRAIN and frozen
for evaluation. It may attenuate or amplify but cannot reverse sign. Float64 endpoint saturation
is allowed/recorded rather than silently clipped. Original classifier/normalizer remain unchanged.

Temporary instance hooks retain autograd on BOTH r/a,verify actual old sum r+a on every forward,
and replace it only after C278's own dynamic norm hook. Full original assertions remain active.
The wrapper restores hook registries on success/exceptions. Control returns None at the late hook.
Require exact plain/control/candidate initial logits and common gradients at runtime preflight;
require each pair's first CE and common pre-clip gradient hash to match in science. Candidate g
participates in global clipping;later parameter trajectories need not coincide. No causal attribution
or unique component-importance interpretation of learned alpha. Model weights can also rescale.

Actual C278 model14256 parameters;candidate14257 with one extra learned scalar. Width16,48tokens,
CPUfloat64,2threads,deterministic. All original parameters train;core/read computations remain.
Ordinary mean CE only,AdamW lr.005,betas.9/.999,eps1e-8,weight_decay0,clip1,one optimizer800steps.
Global fit Torch RNG602000 reset per fit.200epochs*4;96 intact query pairs,24pairs/48rows per update;
private permutation(order+301000+epoch);length=epoch%2;profile=epoch%3. Each row100 exposures per
trained length. Only two/three-character normal TRAIN optimizes weights or g. No HOLDOUT,quad,
masked learning inputs,auxiliary losses,input-conditioned routing or per-query mode selection.

Freeze final models including g;evaluate original2/3/4 normal/evidence-blind/query-blind tasks.
Primary PASS iff all5 learned_gain models pass every old quad criterion. Thresholds unchanged:
accuracy.90,query_pair.80,evidence_drop.35,query_drop.35,two_order.80. Report controls separately;
absolute PASS is not automatic superiority,production adoption,arbitrary-length ability or Gate F.
Retain10results,60 final task/split partitions,30 paired correct-count contrasts,TRAIN/HOLDOUT
flags and final gains. Persist all800 CE/g/alpha histories,final g/alpha,schedules,first common
gradient hashes and raw final logits. No result-dependent gain range,seed,budget or checkpoint selection.

## Parent contract and protection

Verify27 ordered summary hashes BEFORE exact C300.verify_artifacts with26 ancestors and accepted
execution HEAD:C300,C299,...,C274. C300 has4 artifacts and NO dataset copies/trained-model bundle.
Its exact summary seals all4 descriptors;verifier reconstructs all before/after/ablation results.
Require diagnostic PASS,weights/hooks preserved and original full matrices. Read only recursively
verified C299 dataset/triple/quad JSONs and recheck canonical hashes. No parent weights initialize C301.

Sole direct import C300. Its context supplies C299,C294 no-neural,C287 normalization,C284 evaluator/
replay_error,C283 quad,C282 tables/model/core. C296 pair/render helpers are C299.context()[2] and
remain explicitly covered through the inherited map and runtime helper coverage. C301 uses its own
wrapper-aware strict load and counter,not an old fixed-capacity cohort validator. Its candidate
state includes gain_logit plus model.* keys;control has model.* only. Strict replay verifies final
gain,fingerprint and every raw output/argmax with drift<=1e-9. Scoring is unchanged.

Retain all646 parent source pins/1191 inputs;add OWN6 plus5 C300 files:source652/protected1202.
Explicit C278 readout pin0aa8d65874f4a021e21d04948ffd0a1d5615248b is retained. No accepted file edits.
Science:10models,8000updates,384000training rows,9620forwards,539520total rows,38480core calls,
10strict state loads,one10-state bundle read/write,network0. Operational preflight3forward/backward
checks,tests and recursive parent reconstruction are separate. No equal-capacity or speed claim.
Eight outputs plus summary:architecture-plan.json,dataset.json,triple-dataset.json,quad-dataset.json,
trained-models.pt,evaluations.pt,measurements.json,validation-summary.json. Schemas:
fold-c301-gain-models-v1 and fold-c301-gain-eval-v1. Full tensors/maps stay local/ignored;compact logs.
Own40/modules186/loaded4638/focused4637;sole inherited exact C204 exclusion unchanged.
Manifest SHA256:c10f5dd5be005595a12502ff9ebe43802f987464ca1b85da2adb28a47f175dd9.

## Post-authoring review and runtime boundary

post_authoring_review=PASS (separate committed-byte/static review and actual local behavioral tests).
All6 OWN files re-fetched at36156946c5035ba6f52e5973d0f5f9e2ded9898b;whole-file blobs match6/6.
After all matches:normal own40 PASS in9.454s;entire CP932-emulated own40 PASS in9.533s.
Linux/Python3.13.5/PyTorch2.10.0+cpu/NumPy2.3.5. Python2files/3embeddedblocks compile;free globals0;
UTF8/noNUL;manifest matches. Toy800-step fits,finite differences,exact initial gradients,actual
accepted C278 class AST hook integration,frozen strict-gain reload,counting,full production call
ordering,protection/schema validation,serialization/tampering and explicit UTF8 reads pass.
The local support C278 file is a fetched class slice,not a full parent clone,and is not committed.
On the user checkout,test40 extracts that class from the full accepted module. Parent data,Git,
scorers/models and inherited suite members are substituted where unavailable. Toy inputs encode
synthetic targets for software-control tests;they are not scientific learning data or FOLD evidence.
Real Windows27-parent reconstruction,protected bytes,PowerShell ParseFile,real initial forward/
gradient identity,actual4637 regression and10 FOLD training/evaluation/replay runs remain pending.
Activation must preserve all6 reviewed OWN blobs and every accepted source/test/log/dispatcher.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7 after dispatcher ParseFile.
Expected:legacy_dispatcher_pin=PASS -> active_experiment=C301 -> Validate(27parents,652/1202
protection,real initial logits/common-gradient identity,own40,focused4637) ->
authoring_runtime_preflight=PASS -> Execute(10models*800updates,gain learned on TRAIN only,
all old evaluations,strict gain/state reload,persisted reconstruction) -> log publication.
Validate failure skips science/publication. Any scientific integrity problem repairs SAME C301.
Valid all-five candidate miss is ACCEPTED VALID NEGATIVE. Do not change cohort,gain range,initial
gain,LR,budget or thresholds after results. C302 remains unregistered until C301 formal judgment.
Gate F remains NOT PASSED. Separate scientific execution HEAD from log-publication commit.

## Inherited regression compatibility seals

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

Keep accepted legacy seals. Historical lifecycle tests use immutable acceptance addenda.

## Historical state

Full prior handoff:docs/handoff-history/c300-pre-acceptance.md.
Git blob:a0e0da00bd423469dc2c994afebb2b455c4bda7d. Accepted files remain immutable.
Only this Formal state is authoritative;historical ACTIVE commands are not executable.
