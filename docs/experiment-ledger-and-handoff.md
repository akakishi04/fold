# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C195 ACCEPTED PASS. C196 NOT REGISTERED at this acceptance commit.**

C195 execution HEAD:
`485d32b9dba0b0df34709d631a9d454629a1570e`
C195 published log commit:
`2589b6a70873384b8dae3c5932e7d42642478428`
C195 summary SHA:
`614ffe9ee4794f102416bc5e51de1cd9510fde41ec4b43eb436377d9780a9b62`.

C195:1605/1605;85824 episodes; all replay/runtime/status/resource/fake-final errors0;
first reads85824; second34948; third8352; exhausted rows8352; sufficient rows77472.

Claim:
the accepted generic loop handles original budget12 safely and reproduces accepted C191 exactly.

## Next design

C196 one question:
with the generic loop and budget13 held, does initial RETRIEVE permission denial cause exactly
one denied acquisition attempt followed by safe UNRESOLVED termination, with no provider call,
publication, retry, fake evidence or fake SUFFICIENT?

Reference semantics come from accepted C187 permission denial, but C196 tests them inside the
generic multi-step loop.

C197 remains unregistered until C196 judgment.
