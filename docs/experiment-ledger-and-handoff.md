# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C271 ACCEPTED VALID NEGATIVE. C272 ACTIVE / NOT YET JUDGED (PREFLIGHT RECOVERY). C273 NOT REGISTERED.**
C271 valid execution d1c58db43047aceaf82b0108bace9cd731f13b76 passed the pre-science runtime gate
and completed scientific execution. mean_span and endpoint_span each passed0/5 whole-state gates;
both passed4/5 on the original two-character task and0/5 on the unseen three-character task.
C272 is the unique ACTIVE experiment:paired mean-span versus first+last boundary-pair query.

## Latest accepted science — C271

Acceptance:docs/experiment-ledger-addendum-c271-c272.md.
Execution:d1c58db43047aceaf82b0108bace9cd731f13b76.
Published log:de79ff4539e37a7fddff31ff91dc2b40ff77f0c2.
Summary:runs/c271-v5b-query-endpoint-2873a0f5afe04737ab811192ef3caf72/summary.json.
Summary SHA256:4720c3d57d69470ec1bd0564e219dcc3bdd28a555dc6c64e4f73e10b5a1ba05b.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:mean_span0/5;endpoint_span0/5.
Two-character subgate:mean4/5;endpoint4/5.
Triple subgate:mean0/5;endpoint0/5.

Observed complementary pattern:
-endpoint improves shared-prefix triple names substantially;
-endpoint degrades shared-suffix triple names and two-character HOLDOUT;
-mean-span shows the opposite relative tendency.
This motivates a symmetric first+last boundary query but does not prove an internal mechanism.

C270 remains ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded trained-name scope.
Gate F NOT PASSED.

## Active C272 — paired query boundaries

Experiment:C272-v5b-paired-query-boundaries.
Stage:V5-B-PAIRED-QUERY-BOUNDARIES.
Registration:docs/experiment-ledger-addendum-c272-preregistration.md.
Design:docs/v5b-query-boundaries-v0.1.md.
Acceptance base:968a77d2a96d28802de38204ef6c45dff99b4ccc.
Parent C271 execution:d1c58db43047aceaf82b0108bace9cd731f13b76.
Parent summary SHA256:4720c3d57d69470ec1bd0564e219dcc3bdd28a555dc6c64e4f73e10b5a1ba05b.

One question:with identical paired CE training,does a query representation using BOTH the first
and final visible query-byte pre-core states preserve the original two-character task while improving
unseen three-character shared-prefix/shared-suffix transfer?

Fresh seeds272001..272005;arms mean_span and boundary_pair.
mean_span is the actual C269 SpanQueryReadout.
boundary_pair has the same14256 parameters,state keys and matched initial tensors;read.query input is
0.5*(first visible query-byte pre-core state + final visible query-byte pre-core state),where both
positions come only from C269.query_span_mask(tokens). One-byte query_blind '?' therefore reduces to
the same single state. No target/entity/profile/split/pair metadata enters model.forward.
Masked pre-core memory,query/key/output maps,score divisor4,PAD masking,Full core,post-core EOS
residual,normalization and decoder remain unchanged.

Training uses exact C267 two-character data SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Use96 same-facts/different-query pairs;randperm seed+272000+epoch;24 pairs/batch;profile=epoch%3.
800 updates=200 complete epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+273000 per arm. Both arms use CE only;AdamW lr.005,betas.9/.999,eps1e-8,
weight_decay0,global clip1;CPU float64,threads2,deterministic.

Evaluate every final state on BOTH:
1.original C267 two-character task;
2.C270 unseen three-character prompt set SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Primary PASS iff all five boundary_pair states satisfy every fixed criterion on both tasks.
mean_span is reference only. Thresholds stay accuracy>=.90,query_pair>=.80,evidence_drop>=.35,
query_drop>=.35,two_order>=.80. HOLDOUT8-row answer cells require8/8.

Workload:10 models;8000 updates;384000 training rows;9080 model forwards;487680 row presentations;
36320 core calls;one10-state bundle write/load;10 strict state loads.
Artifacts:architecture-plan.json,dataset.json,triple-dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json plus summary.json.

Protection/runtime:
-source pins478;
-protected inputs826;
-direct deciding dependencies48;
-own24;
-modules157;
-loaded3694/focused3693;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
The same seal appears in the benchmark and preregistration. Own test24 requires this handoff to contain
the same seal,so source/prereg/handoff disagreement is an executable preflight failure.

## C272 operational preflight recovery

The first C272 invocation at activation HEAD
5c9ff64d9adfc154edc188b25a3699063e25ab4a stopped in Mode Validate.
Own24 completed with one ERROR;scientific execution did not start and no scientific log publication
was attempted. This is an authoring/runtime preflight defect,not a C272 capability result.

Root cause:C272 protected-input accounting had already been corrected to826 in manifest,precheck,
runner,preregistration and handoff,while validate_result retained the stale executable tuple
(478,820). Own test17 intentionally validates an otherwise-correct payload using the registered826
inputs,so the stale duplicate rejected the fixture.

Repair:
-precheck and validate_result now derive expected source/input counts from manifest();
-no executable validator contains a duplicated numeric registration tuple;
-own test21 rejects stale (478,820) and verifies both validators read
 registration["protected_inputs"];
-docs/experiment-authoring-runtime-gate.md now requires manifest() to be the single executable source
 of registration cardinalities.

The scientific manifest itself is unchanged by this repair,so the sealed SHA remains:
89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
Scientific hypothesis,boundary-pair formula,data,seeds,optimizer,budget,gates and workload are
unchanged. C272 remains the same experiment.

Recovery record:docs/experiment-ledger-addendum-c272-preflight-recovery.md.

Recovery static review:
post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 19940f1fe6644f25a623c62e0c2a53fb024e28a6

Compared prior activation5c9ff64d9adfc154edc188b25a3699063e25ab4a to recovery review target:
only C272 benchmark/test plus runtime-policy/recovery docs changed.
Re-fetched recovery blobs:
-source:f7957a4dc9fe6353c0e2b53c9cd3f2e6d299581d
-test:3a5887df7639509c273d867b63e1669b7de69d48
-policy:5f6d1b932f6405c1f17bf0230a28fd48290f98f2
-recovery:c890b9e90567dca9a9e0124452fd81d98c38e4c4

Static review confirms exactly24 own tests;manifest remains sealed as89fd...;the stale478/820 tuple
does not exist in benchmark source;both precheck and validate_result derive counts from manifest;
and test21 enforces this single-source contract.
Complete own24/focused3693 are deliberately not claimed here. Mode Validate remains authoritative.

## C272 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 19940f1fe6644f25a623c62e0c2a53fb024e28a6

Compared C271 accepted-state commit968a77d2a96d28802de38204ef6c45dff99b4ccc to the review target:
only C272 OWN6 paths differ.

Committed OWN6 blobs:
-source:e6712f42b6295c5ae397a28b8595cfc4ed103da9
-test:30fb25805caa8132ed9afe7f47d0ea0a17e83864
-runner:80b0d4865f907c379afcbb2b8faf8ed5b0008cec
-launcher:ae4b5c609fc09ab8826fab828cf64f979cabea57
-prereg:630cf21cef106bd5f554805884dc94e38b50070e
-design:40dd665a0599b13cffceb5e890c3683397db3fc3

Static review confirms exactly24 numbered own tests;three runner Python blocks with argv sets
{1},{},{1,2,3};Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED before scientific logging;
unique ordered scientific phase markers on distinct physical lines;no ast.Call.lineno order test;
parent C271 negative-state contract;478/826 registration split diagnostics;and runtime manifest-seal
test across benchmark/prereg/handoff.

The protected-input count was corrected before final sealing:parent812 + parent summary1 +
seven parent artifacts + OWN6 =826. After that correction the final manifest was independently
recomputed and sealed as89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604.
No manifest-changing source edit follows that seal.

No complete local checkout/PowerShell runtime is available to the reviewer. Therefore own24,
focused3693,PowerShell ParseFile,parent artifact replay and real ten-model training are NOT claimed
executed here. Mode Validate is the authoritative executable authoring gate.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C272 ->
Mode Validate(parent/source/artifact precheck478/826 + sealed manifest,own24,focused3693) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched training,both-task evaluation,strict replay,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace the scientific latest log.
Execute integrity failure retries SAME C272.
If run_execution_valid=True and scientific_status=FAIL,accept a valid negative without retuning.
C273 stays unregistered until C272 is validly judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
