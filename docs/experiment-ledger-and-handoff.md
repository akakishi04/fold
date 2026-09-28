# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C275 ACCEPTED PASS (diagnostic integrity only). C276 ACTIVE / NOT YET JUDGED (PREFLIGHT RECOVERY). C277 NOT REGISTERED.**
C275 execution3cd34c37a4329f8b8a030f320f1eeefa303706e4 is authoritative.
C275 PASS means saved gate-failure audit integrity only;capability_gate_applicable=False.
C276 is the unique ACTIVE capability experiment:final_boundary lr0.005 versus lr0.0025.
No Gate F promotion,production adoption,seed selection or C277 registration.

## Latest accepted science — C275

Acceptance:docs/experiment-ledger-addendum-c275-c276.md.
Execution:3cd34c37a4329f8b8a030f320f1eeefa303706e4.
Published log:9308dc7fac2a6e298f2e2dbb1b02b9caf2d96649.
Summary:runs/c275-v5b-gate-failure-audit-fb5be8dc32064545aa7a993b70e50706/summary.json.
Summary SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False;model_forward_calls=0.
Primary final-boundary triple failure records=100;near-seed23;broad-seed77.

Primary criterion counts:
-accuracy69;
-query_pair_accuracy69;
-evidence_drop43;
-query_drop33;
-two_order_accuracy31.

Near-seed criterion counts:
-274001 accuracy4,query_pair4,evidence_drop3,query_drop3,two_order2;
-274002 accuracy4,query_pair4,two_order1;
-274004 accuracy6,query_pair6,query_drop2,two_order3;
-274005 accuracy3,query_pair3.
Thus answer/query-pair failures are common to every near-passing seed;mask-drop failures are not.
Seed274003 is a broad failure across all criterion classes.

C274 remains ACCEPTED PASS for diagnostic integrity only.
C273/C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in bounded scope.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## Active C276 — final-boundary optimizer reliability

Experiment:C276-v5b-final-boundary-lr-reliability.
Stage:V5-B-FINAL-BOUNDARY-LR-RELIABILITY.
Registration:docs/experiment-ledger-addendum-c276-preregistration.md.
Design:docs/v5b-final-boundary-lr-reliability-v0.1.md.
Acceptance base:2dac538eb6bc2755a589d9d9ec26135773ade4d7.
Parent C275 execution:3cd34c37a4329f8b8a030f320f1eeefa303706e4.
Parent summary SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb.
C274 parent summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.

One question:does fixed AdamW lr0.0025 improve fresh-seed reliability of the final_boundary
architecture relative to lr0.005,with architecture,data,loss,800-step budget and fixed gates held?

Fresh seeds276001..276005;arms lr005 and lr0025.
Both arms use the exact C274 final-boundary SingleBoundaryReadout with14256 parameters.
Within each seed they start from identical state_dict values and identical paired minibatch order.
The ONLY registered training-policy difference is AdamW learning rate0.005 versus0.0025.

Training uses exact C267 two-character data SHA256
1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1.
Use96 same-facts/different-query pairs;randperm seed+276000+epoch;24 pairs/batch;profile=epoch%3.
800 updates=200 epochs;each TRAIN row200 exposures;profile updates268/268/264.
Fit RNG seed+277000 reset per arm.
Both use mean CE only,AdamW betas.9/.999,eps1e-8,weight_decay0,global clip1;
CPU float64,threads2,deterministic. No early stopping,extra steps,seed replacement or checkpoint selection.

Evaluate every final state on BOTH:
1.original C267 two-character task;
2.C270 unseen three-character dataset SHA256
432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73.

Fixed thresholds remain:
accuracy>=.90,query_pair>=.80,evidence_drop>=.35,query_drop>=.35,two_order>=.80.

Primary PASS iff all five lr0025 states pass every original and triple criterion.
lr005 is matched control only and cannot rescue/fail candidate.

Workload:10 models;8000 updates;384000 training rows;9080 model forwards;487680 row presentations;
36320 core calls;one10-state bundle write/load;10 strict state loads;new_checkpoint_writes1.

Protection/runtime:
-source pins502;
-protected inputs878;
-direct deciding dependencies52;
-own24;
-modules161;
-loaded3790/focused3789;
-sole inherited exact C204 exclusion unchanged.

Final sealed manifest SHA256:
312ed892ba64ef1b0289506d44d1e3da05eec6ee85e67b1d3b21cee282e18355.
The same seal appears in benchmark and preregistration. C276 own test24 requires current handoff
agreement while ACTIVE,then immutable c276-c277 acceptance addendum after acceptance.
Registration cardinalities are manifest-derived at runtime.

## C276 operational preflight recovery

The first C276 invocation at activation HEAD
a5ce13504f6a1a6d77e262cde43766030908b922 stopped in Mode Validate during own24.
test_16_parent_loader_requires_exact_c275_pass raised ValueError:parent hash.
Scientific execution did not start and no scientific log was published.

Root cause:production C276.load_parent correctly verifies two different parent hashes
(C275 summary and C274 summary),but own test16 used one constant-return audit.sha mock for both paths.
The test fixture therefore violated the real multi-parent provenance contract.

Repair:
-test16 now maps p->PARENT_SHA and q->C274_SHA;
-it asserts that both parent identities were queried independently;
-it contains a negative test where the secondary parent returns the wrong hash and requires
 ValueError:parent hash;
-docs/experiment-authoring-runtime-gate.md now includes the Multi-parent fixture fidelity rule;
-production scientific source and manifest are unchanged.

Recovery record:docs/experiment-ledger-addendum-c276-preflight-recovery.md.

Recovery static review:
post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 62ed0b08abdb460f6d5cd60c1e187ff2b4123b55

Compared prior activation a5ce13504f6a1a6d77e262cde43766030908b922 to recovery review target:
only C276 own test16,runtime-policy text and the recovery addendum changed.
Re-fetched recovery blobs:
-source scientific code unchanged:5f7b76dace80698142790ec1ce58cad56cb5f557
-test:c89f0945ee2623e9318d04e7ad5b8c411375487d
-policy:a1078829c9b2a009d87738f11e78a599f4d000f9
-recovery:01cf471f9faeb9d1731e0d9f1f5b81483706a591

The C276 manifest function is unchanged,so the sealed SHA remains:
312ed892ba64ef1b0289506d44d1e3da05eec6ee85e67b1d3b21cee282e18355.
Complete own24/focused3789 are deliberately not claimed here. Mode Validate remains authoritative.

## C276 post-authoring review

post_authoring_review = STATIC PASS / RUNTIME GATE PENDING
review_target_HEAD = 62ed0b08abdb460f6d5cd60c1e187ff2b4123b55

Compared C275 acceptance2dac538eb6bc2755a589d9d9ec26135773ade4d7 to review target:
only C276 OWN6 paths differ.

Committed OWN6 blobs:
-source:5f7b76dace80698142790ec1ce58cad56cb5f557
-test:0cb5135a5732619433b287526b17bffc25833b2f
-runner:3b9238f02ac9acc06580d98fbbb72dbd5d632726
-launcher:29fbfb83ec9c01be3a90ecec4b8c8adf4f0b6c3f
-prereg:3886132b53e4a0e6d8d74c816f68a6357aa2a2ea
-design:efc68963ee2951f7bce0e155ee70bb33ffbfe0c9

Static review confirms exactly24 own tests;three runner embedded Python blocks with argv sets
{1,2},{},{1,2,3,4};Validate before Execute;AUTHORING_RUNTIME_PREFLIGHT_FAILED before scientific
logging;unique ordered run phase markers;manifest-derived502/878 registration;matched architecture/
initial state/batches;the sole registered optimizer difference0.005 versus0.0025;parent C275/C274
provenance;and lifecycle-aware own seal plus legacy C272 compatibility seal.

No complete local checkout/PowerShell runtime is available to reviewer. Therefore own24,
focused3789,PowerShell ParseFile,parent artifact replay and real ten-model training are NOT claimed
executed here. Mode Validate is authoritative.

## Execution and stop

Use tools/invoke_active_v2.ps1 through explicit PowerShell7.
Expected order:
legacy_dispatcher_pin=PASS -> active_experiment=C276 ->
Mode Validate(parent/source/artifact precheck502/878 + sealed manifest,own24,focused3789) ->
authoring_runtime_preflight=PASS ->
Mode Execute(10-model matched lr training,both-task evaluation,strict replay,persisted postcheck) ->
log publication.

Validate failure is operational and must not publish/replace scientific latest log.
Execute integrity failure retries SAME C276.
If run_execution_valid=True and scientific_status=FAIL,accept a valid negative without trying another lr.
C277 stays unregistered until C276 is judged. Gate F NOT PASSED.
Preserve tools/run_c167.ps1,historical tools/invoke_active.ps1,and all accepted evidence/recovery logs.
