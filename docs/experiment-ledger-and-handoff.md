# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C196 ACCEPTED PASS. C197 NOT REGISTERED at this acceptance commit.**

C196 execution HEAD:
`c1a4e68c785fab6441dd08892588add81f9486d6`

C196 published log commit:
`5a2605a9bac234a605b9f35394520fff2175db82`

C196 summary SHA:
`b0de25067be3fb9ab24486e2936a62b26f6cf0446f3b85f7e97f7cb932d7e6fb`.

C196:1629/1629; two85824-episode arms.
ALLOWED reproduces accepted C194 exactly.
PERMISSION_REVOKED_AFTER_DECISION:85824 learned decisions,85824 permission denials,
provider calls/publications/receipts/retries all0, all scientific/resource errors0.

Claim:
generic loop continuation is conditioned on actual OBSERVATION_ADMITTED publication, not merely
on a learned acquisition attempt. Dynamic permission revocation after the learned decision is
contained safely.

## Next design

C197 one question:
if the first acquisition passes authority/reservation but the provider raises ProviderFailure on
the single real call, does the same result-aware loop stop unresolved with no evidence, retry or
fake completion?

Hold models, budget13, cohort, coherent worlds and learned initial decisions fixed.
C198 remains unregistered until C197 judgment.
