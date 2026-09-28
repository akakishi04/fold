# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C276 ACCEPTED VALID NEGATIVE. C277 NOT REGISTERED.**
C276 execution1f1ddd09815cfcd644e90042b83aba085e40e5bb is authoritative.
lr0.005 passed0/5 whole-state and lr0.0025 passed0/5;two-character subgate4/5 versus5/5;
three-character subgate0/5 versus0/5. candidate_gate=False.
C275/C274 remain ACCEPTED PASS for diagnostic integrity only;C273/C272/C271/C270 remain ACCEPTED
VALID NEGATIVE;C269 remains ACCEPTED PASS in bounded scope.
No Gate F promotion,production adoption,post-hoc LR change or C278 registration.

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
C277 is not yet registered.

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

## C276 accepted scope and next boundary

C276 registration/recovery/runtime details remain in its design,preregistration,recovery record and
prior handoff at1f1ddd09815cfcd644e90042b83aba085e40e5bb.

C276 is now ACCEPTED VALID NEGATIVE. lr0.0025 stabilizes the original two-character task but does
not solve the complete three-character gate and worsens aggregate shared-suffix collapse.
The next question is a saved-output criterion audit comparing both C276 learning-rate arms before
any further optimizer or architecture intervention. C277 is not yet registered.
Validate->Execute,manifest sealing,manifest-derived registration counts,mutable-handoff lifecycle,
multi-parent fixture fidelity and inherited compatibility seals remain mandatory. Gate F NOT PASSED.
