# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C199 ACCEPTED PASS. C200 ACTIVE / NOT YET JUDGED. C201 NOT REGISTERED.**

## Accepted C199

Scientific execution HEAD:
`48100f36f4f1acdf44d5cb1d508b907e19724c10`

Published log commit:
`e22618047914b903dc6d459ba0617c05c4fa755b`

Log SHA256:
`8d51629d4d597dc8c111b70443ae332ba45bb5a21eae0b193bf10194c8717318`

Summary SHA256:
`0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9`

C199 deciding result:
- focused regression **1701/1701**
- ATTEMPT_LIMIT rows **34948**
- SUFFICIENT-after-first rows **50876**
- first provider reads **85824**
- second provider calls0
- second publications0
- no third learned decision
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: with max_dispatches changed only from3 to1, the accepted generic loop admits
the first acquisition and safely stops a required second dispatch as ATTEMPT_LIMIT without
second provider work or fabricated completion.

## Gate E readiness blocker addressed by C200

Gate E v0.1 requires RETRIEVE / OBSERVE / ASK_USER task families. The accepted learned path
through C199 learns necessity and fact target, but its v1 policy input has no fact-specific
acquisition-channel binding.

C200 adds that missing visible input boundary without changing v1.

## Active C200

Experiment:
`C200-v5e-acquisition-channel-input`

Stage:
`V5-E-ACQUISITION-CHANNEL-INPUT`

Interface:
```text
v2 features[0:72]  = exact canonical v1 packet
v2 features[72:84] = 4 fact slots x
                      [RETRIEVE, OBSERVE, ASK_USER] eligibility
```

Channel eligibility is semantic applicability only. Existing v1 availability/permission masks
remain separate runtime authority.

Registered diagnostics:
- mask roundtrips32;
- runtime authority cross448;
- hidden-completion pairs12;
- malformed cases18.

Fixed PASS requirements:
- roundtrip failures0;
- runtime-cross failures0;
- hidden packet mismatches0;
- answer-changing hidden pairs6;
- malformed rejected18;
- v1 width72;
- v2 width84;
- exact v1 prefix preservation;
- all8 channel masks representable.

Scope:
- training0;
- fresh seeds0;
- learned forward calls0;
- network/provider/tool execution0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

Authoring:
- expected regression **1731 =1701+30**
- expected modules **85**
- source pins8
- protected inputs9
- artifacts5
- manifest
  `af65cbab8b4e9d594fc4ffad5709acee07a5c85bc91a9148771c1dfe64de13bb`

C200 is an input-contract diagnostic only. It does not claim learned tool selection.

## Stop condition

Judge C200 before any C201 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/import/regression/incomplete/protection failure -> INVALID / RETRY SAME C200.

Gate E remains NOT PASSED.
