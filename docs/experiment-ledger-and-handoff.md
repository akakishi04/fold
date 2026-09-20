# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C199 ACCEPTED PASS. C200 NOT REGISTERED.**

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

Accepted claim: with max_dispatches changed only from3 to1, the accepted generic loop
admits the first acquisition and safely stops a required second dispatch as ATTEMPT_LIMIT,
without second provider work or fabricated completion.

## Gate E readiness blocker

The Gate E v0.1 scope requires RETRIEVE / OBSERVE / ASK_USER families.
The current learned path learns necessity and fact target, but its scientific orchestration
uses RETRIEVE as the acquisition action. Structured task input v1 contains global tool
availability/permission but no fact-specific channel binding, so a learned policy cannot
distinguish retrievable, sensor-only and user-only facts from the numeric input alone.

## Next boundary

C200 is not yet registered at this handoff boundary.

Next one-question intervention:
add an opt-in structured task input v2 that preserves the existing72-feature v1 packet as an
exact prefix and appends3 visible acquisition-channel eligibility bits per fact
(RETRIEVE/OBSERVE/ASK_USER). Hidden values, answer/necessity labels and evaluator dependency
must remain absent; runtime availability/permission remains a distinct layer.

C200 must pass the experiment authoring quality gate before it is described as executable.

Gate E remains NOT PASSED.
