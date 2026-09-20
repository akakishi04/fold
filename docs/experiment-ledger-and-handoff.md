# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> and post-authoring review pass apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C200 ACCEPTED PASS. C201 ACTIVE / NOT YET JUDGED. C202 NOT REGISTERED.**

## Accepted C200

Scientific execution HEAD:
`11181a355f13e7be2fda3957b9cdd45ad8868316`

Published log commit:
`2694d336c11b2f98d5e9f89ed5442d445ac1d45e`

Log SHA256:
`75b48cc324db807542b0cd03a65ac182c40ca6113fcf9ddd77303db958eba04d`

Summary SHA256:
`624889546c9b484003e3f2bc79c1d746de28ea168def13da1a2dc87fde73520e`

C200 deciding result:
- focused regression **1731/1731**
- mask roundtrips32
- runtime authority cross448
- hidden pairs12
- malformed rejected18
- roundtrip/runtime-cross failures0
- hidden packet mismatches0
- answer-changing hidden pairs6
- v1 width72 / v2 width84
- v1 prefix preserved True
- candidate_gate_passed True
- run_execution_valid True
- training/learned-forward/provider/network activity0
- production runtime modified False

The earlier C200 attempt at
`4334bf492fe4d98e22165bb785edf3bcc9def254`
remains INVALID execution only.

Accepted claim: structured-task-input-v2 exposes fact-specific
RETRIEVE/OBSERVE/ASK_USER eligibility as a strict12-bit tail while preserving the canonical
v1 72-feature prefix and separate runtime authority.

## Active C201

Experiment:
`C201-v5e-selected-fact-channel-route`

Stage:
`V5-E-SELECTED-FACT-CHANNEL-ROUTE`

One question:
can accepted C199 learned phase0 fact targets be mapped through exactly-one v2 channel metadata
into the correct typed ActionProposal without changing the selected fact or absorbing runtime
authority into the mapper?

Reference mapper:
`fold_lm/v05/structured_action_channel.py`

Registered route workload:
-9 accepted target blocks;
-9536 episodes/block;
-3 channel variants;
-**257472 route cases** total;
-108 aggregate route records.

Required channel totals:
- RETRIEVE85824
- OBSERVE85824
- ASK_USER85824
- route mismatches0

Authority cross:
-12 cases;
- pending3;
- permission denied6;
- provider unavailable3;
- failures0.

Already-observed controls:
-3;
- all DENIED / ALREADY_OBSERVED.

Invalid mapper controls:
-7/7 rejected.

Scope:
- training0;
- fresh seeds0;
- learned forward calls0;
- provider/network/evidence-write0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

Authoring:
- expected regression **1759 =1731+28**
- expected modules **86**
- source pins15
- protected inputs23
- artifacts5
- manifest
  `615e3aa8374650ae95c889c6e6d9de4b6a5a076327e06838ccae1b74eb71df25`

## Post-authoring review

**post_authoring_review = PASS**

implementation review HEAD:
`ba9759785254839892439814d695312ae65bf266`

The review re-fetched committed remote bytes and checked the helper/benchmark/tests/runner/launcher/
preregistration/docs, parent C200/C199 identities and artifact schema, 28-test definition count,
86-module/1759-test runner contract, py_compile inputs, source/protected counts, manifest identity,
launcher run paths, ExpectedHead/log publication wiring, stale C-number/HEAD/path residue, and
runtime-authority separation.

## Stop condition

Judge C201 before any C202 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/import/regression/incomplete/protection failure -> INVALID / RETRY SAME C201.

Gate E remains NOT PASSED.
