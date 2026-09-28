# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C272 ACCEPTED VALID NEGATIVE. C273 ACTIVE / NOT YET JUDGED (PREFLIGHT RECOVERY). C274 NOT REGISTERED.**
C272 execution8142385889335b778f49963bb4b55570165aeb26 is authoritative for science.
boundary_pair passed0/5 whole-state and0/5 triple gates;two-character subgate4/5.
C273 is the unique ACTIVE experiment:paired boundary_pair versus dual_boundary attention.
No Gate F promotion,production adoption,post-hoc seed rescue or C274 registration.

## Inherited regression compatibility seals

This section is append-only while the corresponding accepted/pinned tests remain in focused
regression. Do not remove an entry merely because a later experiment becomes ACTIVE.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is already accepted/pinned and unconditionally checks the current handoff for this
seal. Editing that accepted test would violate parent provenance,so the compatibility seal is
retained here. C273 and later tests use lifecycle-aware own-seal checks instead:current handoff while
ACTIVE,immutable acceptance addendum after acceptance.

## Latest accepted science — C272

Acceptance:docs/experiment-ledger-addendum-c272-c273.md.
Execution:8142385889335b778f49963bb4b55570165aeb26.
Published log:d0fe2095579280a1d12789bfae96cd7924a00956.
Summary:runs/c272-v5b-query-boundaries-db1ee90fff94483191730b4a6e711da6/summary.json.
Summary SHA256:0955fb7f6af7400aa08799a1f369f9acc7f6730a9401478c4283401d89693f12.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:mean_span0/5;boundary_pair0/5.
Two-character subgate:mean4/5;boundary4/5.
Triple subgate:mean0/5;boundary0/5.

C272 boundary_pair substantially reduced collapse and improved shared-prefix transfer.
Candidate HOLDOUT triple correct/collapse:
-tripled426/480;6/240
-shared_prefix2 426/480;7/240
-shared_suffix2 387/480;32/240
It still fails the strict gate,especially shared_suffix2,and fresh seed272005 is a broad reliability miss.
The other four boundary states preserve two-character HOLDOUT perfectly but still miss at least one
triple criterion. This supports a structural next question rather than seed rescue.

C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded trained-name scope.

## Active C273 — paired dual-boundary attention

Experiment:C273-v5b-paired-dual-boundary-attention.
Stage:V5-B-PAIRED-DUAL-BOUNDARY-ATTENTION.
Registration:docs/experiment-ledger-addendum-c273-preregistration.md.
Design:docs/v5b-dual-boundary-attention-v0.1.md.
Acceptance base:ced412ce712fae1d3de1fdfdb2b12cc0ef41f3f5.
Parent C272 execution:8142385889335b778f49963bb4b55570165aeb26.
Parent summary SHA256:0955fb7f6af7400aa08799a1f369f9acc7f6730a9401478c4283401d89693f12.

One question:does keeping FIRST and FINAL visible query-boundary signals separate through their
attention softmaxes,then averaging retrieved memories,improve reliable original/two-character and
unseen/three-character binding relative to averaging the boundary states before attention?

Fresh seeds273001..273005;arms boundary_pair and dual_boundary.
boundary_pair is the actual C272 BoundaryPairReadout.
dual_boundary has the same14256 parameters,state keys and matched initial tensors.
It computes q_first and q_last with the SAME read.query weights,uses the SAME read.key memory to
create two separately masked attention softmaxes,retrieves memory_first and memory_last,then averages
those memories and applies the shared read.output once. Post-core residual and decoder are unchanged.
For one-byte query-blind '?' the two paths are identical. No target/entity/profile/split/pair metadata
enters model.forward.

Training uses exact C267 two-character data SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Use96 same-facts/different-query pairs;randperm seed+273000+epoch;24 pairs/batch;profile=epoch%3.
800 updates=200 complete epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+274000 per arm. Both use CE only;AdamW lr.005,betas.9/.999,eps1e-8,
weight_decay0,global clip1;CPU float64,threads2,deterministic.

Evaluate every final state on BOTH:
1.original C267 two-character task;
2.C270 unseen three-character prompt set SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Primary PASS iff all five dual_boundary states satisfy every fixed criterion on both tasks.
boundary_pair is reference only. Thresholds stay accuracy>=.90,query_pair>=.80,evidence_drop>=.35,
query_drop>=.35,two_order>=.80. HOLDOUT8-row answer cells require8/8.

Workload:10 models;8000 updates;384000 training rows;9080 model forwards;487680 row presentations;
36320 core calls;one10-state bundle write/load;10 strict state loads.
Artifacts:architecture-plan.json,dataset.json,triple-dataset.json,trained-models.pt,evaluations.pt,
measurements.json,validation-summary.json plus summary.json.

Protection/runtime:
-source pins484;
-protected inputs840;
-direct deciding dependencies49;
-own24;
-modules158;
-loaded3718/focused3717;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
fd38d800c08dcf7fb783f6f5c156169e75b29b1208c175d32259e2d4c77eea7f.
The same seal appears in benchmark and preregistration. Own test24 requires handoff agreement.
Registration cardinalities are manifest-derived at runtime.

## C273 operational preflight recovery

The first C273 invocation at activation HEAD
a63c9aaa7b41fa109542da1be4f6b5789fb717a0 stopped in Mode Validate after own24 PASS, during
focused3717 regression. Scientific execution did not start and no scientific log was published.

Root cause:the inherited accepted C272 test24 unconditionally requires the C272 manifest seal in the
CURRENT mutable handoff. That assertion was valid while C272 was ACTIVE,but the C273 activation
handoff omitted the old seal. The focused regression therefore failed even though C273's own tests
and scientific code were valid.

The accepted C272 test is pinned by parent provenance and is not modified. Recovery instead:
-retains the C272 seal permanently in the append-only compatibility section above;
-makes C273 own test24 lifecycle-aware for its OWN seal:handoff while C273 is ACTIVE,immutable
 c273-c274 acceptance addendum after acceptance;
-adds a C273 own24 check for the legacy C272 compatibility seal,so accidental removal is caught
 before the multi-minute focused suite;
-records the general mutable-handoff lifecycle rule in docs/experiment-authoring-runtime-gate.md.

Recovery record:docs/experiment-ledger-addendum-c273-preflight-recovery.md.
Scientific hypothesis,dual-boundary architecture,data,seeds,training policy,gates,workload and sealed
manifest are unchanged. C273 manifest remains:
fd38d800c08dcf7fb783f6f5c156169e75b29b1208c175d32259e2d4c77eea7f.

Recovery static review:
post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 615478bf853d5be3b9a2653ed49aeff9e5a36788

Compared prior activation a63c9aaa7b41fa109542da1be4f6b5789fb717a0 to recovery review target:
only C273 own test24, runtime-policy text and the recovery addendum changed. C272 accepted source/test
files were not modified. Parent C272 does not pin the runtime-policy or handoff files.
The C273 manifest function is unchanged,so its seal remains valid.

## C273 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 615478bf853d5be3b9a2653ed49aeff9e5a36788

Compared C272 acceptance ced412ce712fae1d3de1fdfdb2b12cc0ef41f3f5 to review target:
only C273 OWN6 paths differ.

Committed OWN6 blobs:
-source:477f705395e927b9ec3efc3ee250afb8f7f950ec
-test:6e829fd4833b458f6c262b8374ba229abfa0e1b6
-runner:c09dc109434e898af5b41b647af68d7cd0e64700
-launcher:8c530b1af1af2fa54eb43cc7ce306312321a1553
-prereg:cbc9d19503c07c50f2ef0e4e88e8456f0ac7507a
-design:f6f83680ef23a94642a4a122c4875bc8cbddbc47

Static review confirms exactly24 own tests;three runner Python blocks with argv sets{1},{},{1,2,3};
Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED before scientific logging;unique ordered
scientific phase markers on distinct lines;manifest-derived484/840 registration;parent C272 negative
contract;and separate first/last softmaxes whose retrieved memories are averaged before one output.

No complete local checkout/PowerShell runtime is available to the reviewer. Therefore own24,
focused3717,PowerShell ParseFile,parent artifact replay and real ten-model training are NOT claimed
executed here. Mode Validate is the authoritative executable authoring gate.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C273 ->
Mode Validate(parent/source/artifact precheck484/840 + sealed manifest,own24,focused3717) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched training,both-task evaluation,strict replay,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace the scientific latest log.
Execute integrity failure retries SAME C273.
If run_execution_valid=True and scientific_status=FAIL,accept a valid negative without retuning.
C274 stays unregistered until C273 is validly judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
