# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C196 ACCEPTED PASS. C197 ACTIVE / NOT YET JUDGED. C198 NOT REGISTERED.**

C196 execution HEAD:
`c1a4e68c785fab6441dd08892588add81f9486d6`
C196 acceptance commit:
`561cc91eaaa219a0c627a79b249aa07d76ad759b`
C196 summary SHA:
`b0de25067be3fb9ab24486e2936a62b26f6cf0446f3b85f7e97f7cb932d7e6fb`.

C196:1629/1629; ALLOWED exact C194 replay; permission-revoked arm85824 safe denials;
provider/publication/receipt/retry all0.

## Active C197

One orchestration change:
for a non-admitted acquisition, use `dispatch.reason` when dispatch exists; otherwise use
`action.reason`.

Arms:
1. ALLOWED — exact accepted C196/C194 replay.
2. PROVIDER_FAILURE_AFTER_RESERVATION — same learned initial decision and SourceBinding,
   successful reservation, one provider call raising ProviderFailure.

Failure-arm required outcome:
- action PENDING/ACQUISITION_RESERVED;
- dispatch UNRESOLVED/PROVIDER_FAILURE;
- orchestration status UNRESOLVED_ACQUISITION_PROVIDER_FAILURE;
- one provider call;
- zero publication/receipt/retry/fact mutation/fake sufficient;
- final resources internal9/acquisitions3/available1/permitted1/outcomeNONE/step11.

Expected regression1653;82 modules.
Source pins146;protected paths385;artifacts5.
Manifest:
`7f7121c336e68dc58578e35f75b7c459986f5adbd2329344fc08514e468d58d2`.

C198 remains unregistered until C197 judgment.
