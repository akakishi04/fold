# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C271 ACCEPTED VALID NEGATIVE. C272 NOT REGISTERED.**
Recovered C271 execution d1c58db43047aceaf82b0108bace9cd731f13b76 is authoritative for science.
mean_span passed0/5 whole-state gates and endpoint_span also passed0/5.
Both arms passed4/5 on the original two-character task and0/5 on the unseen three-character task.
C270 remains ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.
No Gate F promotion,production adoption,post-hoc seed rescue or C273 registration.

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
C272 is not yet registered.

## Latest accepted science — C270

Acceptance:docs/experiment-ledger-addendum-c270-c271.md.
Execution:456deac490990f4c7f4ceb1cdf241f0c606a77de.
Published log:e3670602568ad402d49108e6529dd4b728c2e6e8.
Summary:runs/c270-v5b-triple-identifiers-87c6c92aaa194dada7aae2b420dba776/summary.json.
Summary SHA256:117c55f5498dec1b5e60c2a59fc571eeb485a3f6614f710348e29348e3433d5b.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:eos_query0/5;span_query0/5.

Aggregate C270 candidate span_query:
-TRAIN tripled960/960,collapse0/480;
-TRAIN shared_prefix2 793/960,collapse167/480;
-TRAIN shared_suffix2 906/960,collapse43/480;
-HOLDOUT tripled480/480,collapse0/240;
-HOLDOUT shared_prefix2 381/480,collapse76/240;
-HOLDOUT shared_suffix2 446/480,collapse17/240.
Thus length3 alone is not the failure:tripled is perfect,while shared-character composition fails.
This is consistent with mean-pooling dilution but does not prove that mechanism.

The earlier C270 attempt at11ae165db9dbb73239360a20c9c7cf005cd9c19f remains INVALID history.
Recovery/runtime details remain in docs/experiment-ledger-addendum-c270-execution-recovery.md and
docs/experiment-authoring-runtime-gate.md.

## Latest accepted science — C269

Execution:7c44987b4a70f6ed821657f518b81f78bf0a376d.
Published log:1c34b373ad9610dddcab2e7e54294fd5d4fe7cef.
Summary:runs/c269-v5b-query-span-6383f14adbca4283ac10896b67a6c33f/summary.json.
Summary SHA256:a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8.
Acceptance:docs/experiment-ledger-addendum-c269-c270.md.
span_query5/5 versus eos_query4/5 on trained two-character name profiles with held values.

## C271 accepted scope and next boundary

The complete C271 preregistration/review/runtime-gate details remain in:
-docs/experiment-ledger-addendum-c271-preregistration.md
-docs/v5b-query-endpoint-v0.1.md
-docs/experiment-authoring-runtime-gate.md
and prior handoff commit d1c58db43047aceaf82b0108bace9cd731f13b76.

C271 is now ACCEPTED VALID NEGATIVE. Endpoint query improved shared-prefix three-character binding
but degraded shared-suffix and trained two-character behavior. The next question is whether a fixed
boundary-pair query using both first and last visible query-byte states can preserve both sides.
C272 is not yet registered. Validate->Execute remains mandatory. Gate F NOT PASSED.
