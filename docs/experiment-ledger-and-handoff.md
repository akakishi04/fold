# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C195 ACCEPTED PASS. C196 ACTIVE / NOT YET JUDGED. C197 NOT REGISTERED.**

C195 execution HEAD:
`485d32b9dba0b0df34709d631a9d454629a1570e`
C195 acceptance commit:
`988090c3d047eb1360dc06a7e3fb3956027124b3`
C195 summary SHA:
`614ffe9ee4794f102416bc5e51de1cd9510fde41ec4b43eb436377d9780a9b62`.

C195:1605/1605;85824 episodes; budget12 replay exact; exhausted rows8352;
fake final0; unauthorized final inference0; all runtime/resource errors0.

## Active C196

One orchestration change:
generic loop re-enters only after an actually admitted/published acquisition.

Arms:
1. ALLOWED — exact accepted C194 replay under budget13.
2. PERMISSION_REVOKED_AFTER_DECISION — learned iteration0 decision remains on allowed state,
   then trusted refresh revokes RETRIEVE permission before action proposal.

Denied-arm expected:
one decision + one DENIED/PERMISSION_DENIED attempt, no dispatch/provider/publication/receipt/
retry, no fact mutation/fake sufficient, final resources11/4/permission0/outcome2/step9.

Expected regression1629;81 modules.
Source pins141;protected paths374;artifacts5.
Manifest:
`cbbbcdac61d729e6c73a86d6e3c70ed74189db33bb4c9c2ea557becb630a2457`.

C197 remains unregistered until C196 judgment.
