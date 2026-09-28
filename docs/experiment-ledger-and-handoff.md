# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C273 ACCEPTED VALID NEGATIVE. C274 NOT REGISTERED.**
C273 execution1106e0898e1698a06b78ac2266c65a983aded275 is authoritative for science.
boundary_pair passed0/5 whole-state gates and dual_boundary passed1/5.
Both arms passed5/5 on the original two-character task;triple subgate was0/5 versus1/5.
C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.
No Gate F promotion,production adoption,seed selection or C275 registration.

## Latest accepted science — C273

Acceptance:docs/experiment-ledger-addendum-c273-c274.md.
Execution:1106e0898e1698a06b78ac2266c65a983aded275.
Published log:22b74e6a2aba7f265edf68994563f472328af241.
Summary:runs/c273-v5b-dual-boundary-b70af8ffe4b047ee95a0044e86de7a8c/summary.json.
Summary SHA256:0e764c595c64818c308779cd5190883edec0654375c82970641efa70b980f82e.
run_execution_valid=True;scientific_status=FAIL;candidate_gate=False.
Seed pass counts:boundary_pair0/5;dual_boundary1/5.
Two-character subgate:boundary5/5;dual5/5.
Triple subgate:boundary0/5;dual1/5.
C274 is not yet registered.

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

## C273 accepted scope and next boundary

C273 preregistration/recovery/runtime details remain in its design,preregistration,preflight recovery,
runtime-gate documents and prior handoff at1106e0898e1698a06b78ac2266c65a983aded275.

C273 is now ACCEPTED VALID NEGATIVE. The dual-boundary fusion produced one full passing seed but
degraded shared-suffix behavior across the cohort. Before another fusion rule,the next question is a
fresh matched directional diagnostic comparing first-only versus final-only query-boundary states.
C274 is not yet registered. Validate->Execute,manifest sealing,manifest-derived registration counts,
mutable-handoff lifecycle rules,and inherited compatibility seals remain mandatory. Gate F NOT PASSED.
