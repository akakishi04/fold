# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C274 ACCEPTED PASS (diagnostic integrity only). C275 NOT REGISTERED.**
C274 execution90f76a8f017d562caded127821852654b8e3d061 is authoritative.
scientific_status=PASS means the directional diagnostic completed;capability_gate_applicable=False.
first_boundary measured two_char0/5,triple0/5;final_boundary measured two_char4/5,triple0/5.
C273/C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.
No Gate F promotion,capability winner,production adoption or C276 registration.

## Latest accepted science — C274

Acceptance:docs/experiment-ledger-addendum-c274-c275.md.
Execution:90f76a8f017d562caded127821852654b8e3d061.
Published log:acb1236f5299052662525deec2b00f0bb415338b.
Summary:runs/c274-v5b-directional-boundary-06a7a84bf4554f83b5cb6e099a828178/summary.json.
Summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False.
Task pass counts:first_boundary two_char0/5,triple0/5;final_boundary two_char4/5,triple0/5.
C275 is not yet registered.

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

C273 dual_boundary produced one full passing seed(273001) but degraded shared-suffix pooled behavior
relative to boundary_pair. This does not support another fusion change without first measuring the
directional first-only versus final-only components directly.

C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.

## Inherited regression compatibility seals

This section is append-only while the corresponding accepted/pinned tests remain in focused
regression. Do not remove an entry merely because a later experiment becomes ACTIVE.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is already accepted/pinned and unconditionally checks the current handoff for this
seal. Editing that accepted test would violate parent provenance,so the compatibility seal is
retained here. C273 and later tests use lifecycle-aware own-seal checks instead:current handoff while
ACTIVE,immutable acceptance addendum after acceptance.

## C274 accepted scope and next boundary

C274 registration/runtime details remain in its design,preregistration and prior handoff at
90f76a8f017d562caded127821852654b8e3d061.

C274 is now ACCEPTED PASS for diagnostic integrity only. final_boundary broadly outperformed
first_boundary,but all final states still fail the complete triple task despite near-perfect pooled
answers in four seeds. The next question is a saved-output gate-failure audit before any new
architecture intervention. C275 is not yet registered.
Validate->Execute,manifest sealing,manifest-derived registration counts,mutable-handoff lifecycle
rules and inherited compatibility seals remain mandatory. Gate F NOT PASSED.
