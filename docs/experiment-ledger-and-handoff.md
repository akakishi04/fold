# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> and post-authoring review pass apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C201 ACCEPTED PASS. C202 ACTIVE / NOT YET JUDGED. C203 NOT REGISTERED.**

## Accepted C201

Scientific execution HEAD:
`1ce0334e0d5ee76c7e5fac40082c19bd43576415`

Published log commit:
`49a85f2e7cc7a2d4779d354c9adc7e064f61cbfb`

Log SHA256:
`5e19cae5bbac7bd8be9ecb23fd0bf1bbd0e1f1fc3ee376ba5890ccef7c088835`

Summary SHA256:
`c27ff79f20811ce373d175617b2a556c3c847d631f096fb401cb0251ad4fca4c`

C201 deciding result:
- focused regression **1759/1759**
- route cases257472
- route mismatches0
- RETRIEVE/OBSERVE/ASK_USER each85824
- authority cross12 / failures0
- already-observed controls3/3
- invalid mapper7/7 rejected
- candidate_gate_passed True
- run_execution_valid True
- training/learned-forward/provider/network/evidence-write0
- production runtime modified False

Accepted claim: accepted learned fact targets can be preserved exactly while exactly-one v2
channel metadata produces the matching typed ActionProposal, with runtime authority remaining
separate and authoritative.

## Active C202

Experiment:
`C202-v5e-three-channel-acquisition-dispatch`

Stage:
`V5-E-THREE-CHANNEL-ACQUISITION-DISPATCH`

One question:
can each accepted learned target, under each exactly-one RETRIEVE/OBSERVE/ASK_USER variant,
execute through the real structured acquisition lifecycle and publish exactly the selected
coherent-world fact without cross-channel provider work or nonselected fact mutation?

Registered workload:
-9 target blocks;
-9536 targets/block;
-3 channels;
-**257472 acquisitions** total;
-27 block/channel records.

Required channel provider totals:
- RETRIEVE85824
- OBSERVE85824
- ASK_USER85824

Per case:
- typed proposal preserves selected fact;
- ActionResult PENDING / ACQUISITION_RESERVED;
- DispatchResult PUBLISHED / OBSERVATION_ADMITTED;
- only matching channel provider called once;
- selected fact OBSERVED at registered world bit;
- nonselected facts unchanged UNOBSERVED;
- one receipt;
- final resources internal9/acquisitions3/all channels available+permitted/outcome NONE/step11;
- pending none / runtime terminal none.

Fixture:
- in-memory coherent C190 world documents;
- actual lifecycle source/delivery/document/publication validation remains active;
- not a real sensor/user/network transport.

Scope:
- training0;
- fresh seeds0;
- learned forward calls0;
- network0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

Authoring:
- expected regression **1785 =1759+26**
- expected modules **87**
- source pins25
- protected inputs39
- artifacts5
- manifest
  `24bd6b04647342e8114a6e8245af046cfdae242a06d65c0a46286f577267406e`

## Post-authoring review

**post_authoring_review = PASS**

implementation review HEAD:
`8879022df0aa6c904399fea21d7187614378d557`

The review re-fetched committed remote bytes and checked benchmark/tests/runner/launcher/
preregistration/docs, accepted C201/C200/C199 identities, the C199 prediction artifact and four
historical runtime/source pins, 26-test definition count, 87-module/1785-test runner contract,
25 source pins /39 protected inputs, manifest identity, py_compile inputs, all three launcher
parent run paths, ExpectedHead/log publication wiring, provider-channel isolation, fact/resource
postconditions, stale C-number/HEAD/path residue and C203 non-registration.

## Stop condition

Judge C202 before any C203 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/import/regression/incomplete/protection failure -> INVALID / RETRY SAME C202.

Gate E remains NOT PASSED.
