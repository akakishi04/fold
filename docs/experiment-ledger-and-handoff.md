# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C277 ACCEPTED PASS (diagnostic integrity only). C278 ACTIVE / NOT YET JUDGED. C279 NOT REGISTERED.**
C277 execution58ce50ffa45e6e51ebab65417b67bf08ff4b6f33 is authoritative.
C277 PASS means saved failure-profile audit integrity only;capability_gate_applicable=False.
C278 is the unique ACTIVE capability experiment:mean_span versus mean_final_dual.
No Gate F promotion,production adoption,seed selection or C279 registration.

## Latest accepted science — C277

Acceptance:docs/experiment-ledger-addendum-c277-c278.md.
Execution:58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.
Published log:7a46048503459aa7e03982b22c8dc8cf5ad2f976.
Summary:runs/c277-v5b-saved-lr-audit-7e9cad9663144ae9bdbacda802c21306/summary.json.
Summary SHA256:ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False;model_forward_calls=0.

C277 triple criterion delta(candidate-control):
-accuracy -37;
-query_pair_accuracy -37;
-two_order_accuracy -18;
-evidence_drop +3;
-query_drop +1.

Stable/control-good seeds276001/276002/276004/276005 worsen in aggregate:
accuracy+1;query_pair+1;evidence_drop+12;query_drop+15;two_order+3.
The overall lr0.0025 improvement is therefore dominated by broad recovery seed276003.

shared_suffix2 HOLDOUT candidate-control:
accuracy-7;query_pair-7;two_order-5;evidence_drop+4;query_drop+5.
Lower lr improves direct answer/query discrimination but weakens registered mask sensitivity.

C276 remains ACCEPTED VALID NEGATIVE.
C275/C274 remain ACCEPTED PASS for diagnostic integrity only.
C273/C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in bounded scope.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Active C278 — mean-span plus final-boundary dual attention

Experiment:C278-v5b-mean-final-dual-query.
Stage:V5-B-MEAN-FINAL-DUAL-QUERY.
Registration:docs/experiment-ledger-addendum-c278-preregistration.md.
Design:docs/v5b-mean-final-dual-query-v0.1.md.
Acceptance base:8a9340c5165754080ea729cf013b6015035df824.
Parent C277 execution:58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.
Parent C277 summary SHA256:ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13.
C276/C275/C274 parent summary SHA256:
6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f /
1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb /
0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

One question:with identical fresh paired CE training,does keeping the mean visible query-span signal
and final visible query-boundary signal separate through their attention softmaxes,then averaging
retrieved memories,improve reliable two/three-character binding relative to mean-span attention alone?

Fresh seeds278001..278005;arms mean_span and mean_final_dual.
mean_span is the actual C269 SpanQueryReadout.
mean_final_dual has exactly the same14256 parameters/state keys and uses:
-mean visible query-span pre-core state -> shared read.query -> masked attention A;
-final visible query-byte pre-core state -> same read.query -> masked attention B;
-same read.key(local memory);
-memory=(memory_mean+memory_final)/2;
-shared read.output once;
-unchanged post-core residual/readout_norm/decoder.

For a one-byte query,mean and final states are identical,so candidate reduces exactly to the control
attention computation. No supervision metadata enters model.forward.

Training:
-exact C267 two-character dataset SHA256
 1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1;
-96 paired TRAIN groups;
-randperm seed+278000+epoch;
-24 pairs/48 rows per batch;
-profile=epoch%3;
-800 updates/200 epochs;
-each TRAIN row200 exposures;
-profile updates268/268/264;
-fit RNG seed+279000;
-mean CE only;
-AdamW lr0.005,betas.9/.999,eps1e-8,weight_decay0,clip1;
-CPU float64,threads2,deterministic.

Evaluation:
1.original C267 two-character task;
2.C270 unseen three-character task SHA256
 432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Fixed gates remain:
accuracy>=.90;query_pair>=.80;evidence_drop>=.35;query_drop>=.35;two_order>=.80.

Primary PASS iff all five mean_final_dual states pass every original and triple criterion.
mean_span is matched control only and cannot rescue/fail candidate.

Workload:
-models10;
-train_steps8000;
-training_rows384000;
-model_forward_calls9080;
-row_presentations487680;
-core_forward_calls36320;
-one10-state bundle write/load;
-10 strict state loads;
-new_checkpoint_writes1.

Protection/runtime:
-source pins514;
-protected inputs902;
-direct deciding dependencies54;
-own24;
-modules163;
-loaded3838/focused3837;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
791f287f21bcadd6c708496cd6922a2ef82a2ab94d2cf12ab5c3d669e1917dec.
The same seal appears in benchmark and preregistration. C278 own test24 requires current handoff
agreement while ACTIVE,then immutable c278-c279 acceptance addendum after acceptance.
Registration cardinalities are manifest-derived at runtime.

## C278 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 84b562cf8124ea5d5df0cf13bc66c52908745290

Compared C277 acceptance8a9340c5165754080ea729cf013b6015035df824 to review target:
only C278 OWN6 paths differ.

Committed OWN6 blobs:
-source:0aa8d65874f4a021e21d04948ffd0a1d5615248b
-test:2b4fa04bae8e8a595ff65c0ca6922516a24bcb6b
-runner:b6ac1dd52c85873aa845afd2cd073b3f64eff3bb
-launcher:b6f935b0469628f9cd8e45983f2e91bb6798b2d0
-prereg:82180666515009feb53c3c655c222324c127bedd
-design:c2b83e54a170482873d73abeb61191e3c8fab8d1

Static review confirms exactly24 own tests;Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED
before scientific logging;manifest-derived514/902 registration;four parent hashes modeled
independently in source and test fixture;actual C269 SpanQueryReadout control;two separate candidate
softmaxes with shared parameters and post-retrieval averaging;candidate5/5 gate;unique ordered run
phase markers;and lifecycle-aware own seal plus legacy C272 compatibility seal.

No complete user-local runtime is available to reviewer. Therefore own24,focused3837,PowerShell
ParseFile,parent artifact replay and real ten-model training are NOT claimed executed here.
Mode Validate is authoritative.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C278 ->
Mode Validate(parent/source/artifact precheck514/902 + sealed manifest,own24,focused3837) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched training,both-task evaluation,strict replay,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace scientific latest log.
Execute integrity failure retries SAME C278.
If run_execution_valid=True and scientific_status=FAIL,accept a valid negative without another
fusion tweak inside C278.
C279 stays unregistered until C278 is judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
