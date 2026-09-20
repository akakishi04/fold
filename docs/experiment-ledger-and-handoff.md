# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C198 ACCEPTED PASS. C199 ACTIVE / NOT YET JUDGED. C200 NOT REGISTERED.**

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
- stale reservation rows85824
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

Accepted claim: after a successful reservation, a trusted evidence-identity refresh makes the
reservation stale; the generic loop preserves `STALE_RESERVATION`, performs no provider work,
publishes no evidence and does not retry.

## Active C199

Experiment:
`C199-v5e-attempt-limit-generic-loop`

Stage:
`V5-E-ATTEMPT-LIMIT-GENERIC-LOOP`

Single changed condition:
```text
ALLOWED:            AcquisitionOwner max_dispatches = 3
DISPATCH_LIMIT_ONE: AcquisitionOwner max_dispatches = 1
```

The first acquisition remains fully admitted. If the accepted C198 policy still requests a
second acquisition, the second reservation is created but dispatch must return
`DENIED / ATTEMPT_LIMIT`.

Frozen accepted C198 second-request counts:
- total ATTEMPT_LIMIT rows **34948**
- SUFFICIENT-after-first rows **50876**

Required intervention behavior:
- first reads/provider calls/publications/receipts:9536 per block;
- learned decisions:19072 per block;
- attempt_limit_rows exactly equal accepted C198 `second_reads` for that block;
- second provider calls0;
- second publications0;
- no third learned prediction;
- prefix predictions/logits exact to C198 ALLOWED;
- limit rows terminate `UNRESOLVED_ACQUISITION_ATTEMPT_LIMIT`;
- sufficient rows terminate normally;
- no fake completion.

Limit-row final resource contract:
`internal6 / acquisitions2 / available1 / permitted1 / outcome ATTEMPT_LIMIT / step14`.

Sufficient-after-first final resource contract:
`internal8 / acquisitions3 / available1 / permitted1 / outcome NONE / step12`.

Workload:
-2 x85824 episodes;
-9 selector blocks / arm;
-expected regression **1701 =1677+24**;
-expected modules **84**;
-source pins156;
-protected paths407;
-artifacts5;
-no new training/fresh seeds/network/proof checking/answer generation;
-production runtime modified False;
-Gate E candidate False.

Manifest:
`3bda32133c97539c4e327899e08859e57df9361caa50657e22000374e65bacec`

C199 owns the C198 artifact loader and fixes the parent prediction schema before execution.
The integration test uses a real first FileSnapshotProvider acquisition and then exercises the
real owner dispatch limit; learned second-step output is deterministic test scaffolding only,
not scientific benchmark evidence.

## Stop condition

Judge C199 before any C200 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/nonfinite/regression/incomplete/protection failure -> INVALID / RETRY SAME C199.

Gate E remains NOT PASSED.
