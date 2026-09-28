# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C276 ACCEPTED VALID NEGATIVE. C277 ACTIVE / NOT YET JUDGED. C278 NOT REGISTERED.**
C276 execution1f1ddd09815cfcd644e90042b83aba085e40e5bb is authoritative.
lr0.005 passed0/5 whole-state and lr0.0025 passed0/5;two-character4/5 versus5/5;
three-character0/5 versus0/5. candidate_gate=False.
C277 is the unique ACTIVE experiment and is a saved-output diagnostic with zero neural calls.
No Gate F promotion,capability winner,production adoption or C278 registration.

## Latest accepted science — C276

Acceptance:docs/experiment-ledger-addendum-c276-c277.md.
Execution:1f1ddd09815cfcd644e90042b83aba085e40e5bb.
Published log:d6b1fbb566fdb99d0ca8a2d735cd29c64bcd9114.
Summary:runs/c276-v5b-final-boundary-lr-dcd7c7c2f13d49209c05bd4b2ca43110/summary.json.
Summary SHA256:6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:lr0050/5;lr00250/5.
Two-character subgate:lr0054/5;lr00255/5.
Triple subgate:lr0050/5;lr00250/5.

Aggregate C276 HOLDOUT:
-two-char doubled456/480 ->480/480;
-two-char shared_prefix458/480 ->480/480;
-two-char shared_suffix458/480 ->480/480;
-triple tripled455/480 ->480/480;
-triple shared_prefix2449/480 ->478/480;
-triple shared_suffix2400/480 ->404/480.
Lower lr removes the broad control failure at seed276003 and stabilizes two-character retention,
but it does not solve shared-suffix binding or the complete three-character gate.

C275/C274 remain ACCEPTED PASS for diagnostic integrity only.
C273/C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in bounded scope.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Active C277 — saved LR failure-profile audit

Experiment:C277-v5b-saved-lr-failure-profile-audit.
Stage:V5-B-SAVED-LR-FAILURE-PROFILE-AUDIT.
Registration:docs/experiment-ledger-addendum-c277-preregistration.md.
Design:docs/v5b-saved-lr-failure-profile-audit-v0.1.md.
Acceptance base:0544885dc7db8b55b6d12c925ee6454fae88a1ea.
Parent C276 execution:1f1ddd09815cfcd644e90042b83aba085e40e5bb.
Parent C276 summary SHA256:6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f.
C275 summary SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb.
C274 summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

One question:how does lr0.0025 change the exact fixed-gate failure profile relative to lr0.005,
especially shared_suffix2 and the seed276003 recovery?

C277 performs zero training,zero model forwards,zero core calls,zero checkpoint writes and zero
model-state loads. It verifies C276/C275/C274 accepted parent chains with neural Module calls blocked,
reconstructs the accepted C276 measurements exactly,and attributes saved failures only.

Fixed thresholds remain:
-accuracy0.90;
-query_pair_accuracy0.80;
-evidence_drop0.35;
-query_drop0.35;
-two_order_accuracy0.80.

Primary reports:
-all triple criterion-count deltas candidate-minus-control;
-shared_suffix2 TRAIN/HOLDOUT criterion deltas;
-seed276003 criterion delta;
-stable seeds276001/276002/276004/276005 criterion delta;
-per-seed triple criterion deltas.

Formal C277 PASS means diagnostic execution/integrity only:
-C276/C275/C274 parent chain verifies;
-exactly10 C276 metric records reconstruct in registered identity order;
-all fixed pass flags equal reconstructed threshold margins;
-all arm/profile/seed failure aggregates and deltas persist/reconstruct;
-no provenance guard fails.
PASS cannot declare a capability winner or promote Gate F.

Workload:
-model_forward_calls0;
-row_presentations0;
-core_forward_calls0;
-train_steps0;
-new_checkpoint_writes0;
-model_state_loads0.

Artifacts:audit-plan.json,failure-profile.json,validation-summary.json plus summary.json.

Protection/runtime:
-source pins508;
-protected inputs892;
-direct deciding dependencies53;
-own24;
-modules162;
-loaded3814/focused3813;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
50796e76783611eb04649fd47c450f3fe47d05a34fc0c787168fa38e612d8de9.
The same seal appears in benchmark and preregistration. C277 own test24 requires current handoff
agreement while ACTIVE,then immutable c277-c278 acceptance addendum after acceptance.
Registration cardinalities are manifest-derived at runtime.

## C277 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 868f0d2ece1558d96bdbdbffcf35414ad7860ce0

Compared C276 acceptance0544885dc7db8b55b6d12c925ee6454fae88a1ea to review target:
only C277 OWN6 paths differ.

Committed OWN6 blobs:
-source:020267a09a4579a0f96f13a067fb3a161fe84998
-test:217cd0228ec53efb153d0c02d2eb8cb4d6d51280
-runner:7570987c927fef1b00137424d4016b0d2f13fab4
-launcher:d9e77997662e1dac44498574db602f853dd4f900
-prereg:60c3be8ce3463a10e6e89cec2a28649e0a71c084
-design:294a9c96766ce44b78701c279bde23c7bb61eb7c

Static review confirms exactly24 own tests;Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED
before scientific logging;manifest-derived508/892 registration;zero neural workload;C276/C275/C274
hashes modeled independently in source and test fixture;wrong-secondary-parent negative test;
saved criterion-delta reconstruction;and lifecycle-aware own seal plus legacy C272 compatibility seal.

No complete local checkout/PowerShell runtime is available to reviewer. Therefore own24,
focused3813,PowerShell ParseFile,parent artifact reconstruction and saved-audit execution are NOT
claimed executed here. Mode Validate is authoritative.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C277 ->
Mode Validate(parent/source/artifact precheck508/892 + sealed manifest,own24,focused3813) ->
authoring_runtime_preflight=PASS ->
Mode Execute(saved C276 failure-profile attribution only,zero neural calls,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace scientific latest log.
Execute integrity failure retries SAME C277.
If run_execution_valid=True and scientific_status=PASS,accept it as DIAGNOSTIC PASS ONLY.
Use the attribution result to decide C278;do not infer a capability winner from C277.
C278 stays unregistered until C277 is judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
