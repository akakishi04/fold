# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C275 ACCEPTED PASS (diagnostic integrity only). C276 NOT REGISTERED.**
C275 execution3cd34c37a4329f8b8a030f320f1eeefa303706e4 is authoritative.
scientific_status=PASS means saved gate-failure audit integrity only;capability_gate_applicable=False.
Primary final-boundary triple failures=100;all five C274 seeds are covered.
C274 remains ACCEPTED PASS for diagnostic integrity only;C273/C272/C271/C270 remain ACCEPTED VALID
NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.
No Gate F promotion,capability winner,production adoption or C277 registration.

## Latest accepted science — C275

Acceptance:docs/experiment-ledger-addendum-c275-c276.md.
Execution:3cd34c37a4329f8b8a030f320f1eeefa303706e4.
Published log:9308dc7fac2a6e298f2e2dbb1b02b9caf2d96649.
Summary:runs/c275-v5b-gate-failure-audit-fb5be8dc32064545aa7a993b70e50706/summary.json.
Summary SHA256:1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False;model_forward_calls=0.
Primary final-boundary triple failure records=100;near-seed23;broad-seed77.
C276 is not yet registered.

## Latest accepted science — C274

Acceptance:docs/experiment-ledger-addendum-c274-c275.md.
Execution:90f76a8f017d562caded127821852654b8e3d061.
Published log:acb1236f5299052662525deec2b00f0bb415338b.
Summary:runs/c274-v5b-directional-boundary-06a7a84bf4554f83b5cb6e099a828178/summary.json.
Summary SHA256:0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False.
Task pass counts:first_boundary two_char0/5,triple0/5;final_boundary two_char4/5,triple0/5.

Directional aggregate HOLDOUT triple:
-first_boundary tripled392/480,shared_prefix2314/480,shared_suffix2360/480;
-final_boundary tripled432/480,shared_prefix2426/480,shared_suffix2409/480.
final_boundary is broadly stronger,but no final state obtains complete triple PASS.
Near-passing final seeds274001/274002/274004/274005 have pooled triple HOLDOUT280/284/281/288
of288;seed274003 is a broad miss at134/288. The remaining fixed gate failures require attribution.

C273/C272/C271/C270 remain ACCEPTED VALID NEGATIVE;C269 remains ACCEPTED PASS in its bounded scope.

## Inherited regression compatibility seals

This section is append-only while corresponding accepted/pinned tests remain in focused regression.

- C272 manifest seal:
  89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604

C272 own test24 is accepted/pinned and still reads the mutable handoff. Preserve this seal.
C273 and later tests use lifecycle-aware own seals:current handoff while ACTIVE,immutable acceptance
addendum after acceptance.

## C275 accepted scope and next boundary

C275 registration/runtime details remain in its design,preregistration and prior handoff at
3cd34c37a4329f8b8a030f320f1eeefa303706e4.

C275 is now ACCEPTED PASS for diagnostic integrity only. The common near-seed failure signature is
answer accuracy plus query-pair discrimination;mask-drop failures are not common to all near seeds.
The next question is therefore a fresh matched optimizer-reliability test on final_boundary before
introducing another reader/fusion architecture. C276 is not yet registered.
Validate->Execute,manifest sealing,manifest-derived registration counts,mutable-handoff lifecycle
rules and inherited compatibility seals remain mandatory. Gate F NOT PASSED.
