# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C198 ACCEPTED PASS. C199 NOT REGISTERED.**

## Accepted C198

Scientific execution HEAD:
`e5a09864497fa38a9eac8d400b5162e33e99ec0d`

Published log commit:
`49fcb1145acdcf3efd20afb5edf2740585265655`

Log SHA256:
`f8f0de3e15725926bba692dba294b402763c480ac7e63965cda795d6644a0dee`

Summary SHA256:
`9cbb99e6ad200c5a9b88438abf140c58dd293661d8765f3460e3d2a7c70a8e75`

C198 deciding result:
- focused regression **1677/1677**
- ALLOWED 9/9 accepted replay
- STALE_RESERVATION_AFTER_RESERVATION 85824/85824
- stale provider calls0
- stale provider reads0
- publications0
- receipts0
- retries0
- fact mutation0
- fake SUFFICIENT0
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: after successful reservation, a trusted evidence-identity refresh makes the
reservation stale; the generic loop preserves `STALE_RESERVATION`, performs no provider work,
publishes no evidence and does not retry.

## Next boundary

C199 is not yet registered at this handoff boundary.

Next one-question intervention:
hold the accepted learned models, budget13 cohort, source worlds and orchestration fixed, and
change only the trusted AcquisitionOwner dispatch limit from3 to1. After one successful
acquisition, rows that still need another observation should reserve the second acquisition
but dispatch must deny it as `ATTEMPT_LIMIT`, with no second provider call/publication and no
third learned decision. Rows made sufficient by the first observation must still stop normally.

C199 must pass the experiment authoring quality gate before it is described as executable.

Gate E remains NOT PASSED.
