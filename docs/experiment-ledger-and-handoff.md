# FOLD Experiment Ledger and Handoff

Follow AGENTS.md and docs/experiment-conversation-handoff-protocol.md (response format v2).
Repository:akakishi04/fold;branch:feat/sft-target-loss;local:M:\asobiba\fold.
Authoritative runtime:Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.
User execution entry:tools/invoke_active_v2.ps1 through PowerShell7.
Historical tools/invoke_active.ps1 remains immutable/pinned.

## Formal state

Gate A/B PASSED;C/D PASSED in measured scope;Gate E PASSED;Gate F NOT PASSED.

**C277 ACCEPTED PASS (diagnostic integrity only). C278 NOT REGISTERED.**
C277 execution58ce50ffa45e6e51ebab65417b67bf08ff4b6f33 is authoritative.
C277 scientific_status=PASS means saved failure-profile audit integrity only;
capability_gate_applicable=False;model_forward_calls=0.
C276 remains ACCEPTED VALID NEGATIVE.
C275/C274 remain ACCEPTED PASS for diagnostic integrity only;C273/C272/C271/C270 remain ACCEPTED
VALID NEGATIVE;C269 remains ACCEPTED PASS in bounded scope.
No Gate F promotion,capability winner,production adoption or C279 registration.

## Latest accepted science — C277

Acceptance:docs/experiment-ledger-addendum-c277-c278.md.
Execution:58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.
Published log:7a46048503459aa7e03982b22c8dc8cf5ad2f976.
Summary:runs/c277-v5b-saved-lr-audit-7e9cad9663144ae9bdbacda802c21306/summary.json.
Summary SHA256:ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13.
run_execution_valid=True;scientific_status=PASS;diagnostic_complete=True;
capability_gate_applicable=False;model_forward_calls=0.
Triple criterion delta(candidate-control):accuracy-37,query_pair-37,two_order-18,
evidence_drop+3,query_drop+1.
Stable-seed aggregate worsens:accuracy+1,query_pair+1,evidence_drop+12,query_drop+15,two_order+3.
C278 is not yet registered.

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

## C277 accepted scope and next boundary

C277 registration/runtime details remain in its design,preregistration and prior handoff at
58ce50ffa45e6e51ebab65417b67bf08ff4b6f33.

C277 is now ACCEPTED PASS for diagnostic integrity only. Lower lr mainly rescues seed276003 rather
than improving the already-stable cohort,and shared_suffix2 shows an answer-discrimination versus
mask-sensitivity tradeoff. The next question returns to query representation:mean-span plus final
boundary through separate attentions. C278 is not yet registered.
Validate->Execute,manifest sealing,manifest-derived registration counts,mutable-handoff lifecycle,
multi-parent fixture fidelity and inherited compatibility seals remain mandatory. Gate F NOT PASSED.
