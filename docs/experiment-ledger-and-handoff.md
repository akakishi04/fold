# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) applies.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C191 ACCEPTED PASS. C192 ACTIVE / NOT YET JUDGED. C193 NOT REGISTERED.**

C191 execution HEAD:
`f83ed1d60758dc1ff895b2b9c42c69d6a68c0931`
C191 acceptance commit:
`37e2f2c818ec32f6c1281ed8ba8f58c3d07590b4`
C191 summary SHA:
`b05cd702e9572c61a3ae981e5279c7fb096fe1078c7d65f6401f180f307c84f4`.

C191: 1509/1509;85824 episodes; third acquisitions8352; final logical NEEDS0;
fourth decision accepted0; all replay/action/contract counters0.

## C192 invalid-attempt recovery

First C192 attempt at execution HEAD `0c83f43c85dd535deb3fcccc2310a8e3d215f3a4`
is **INVALID EXECUTION / RETRY SAME C192**. Precheck and all1533 tests passed. Benchmark
stopped before block1 because the C192 run path accidentally used
`c191.load_parent_predictions()`, which expects the C190 parent NPZ schema, instead of
C192's own loader for the C191 output schema.

Published log commit `e2a136ee81d861ea81b48d12697891ff42aca3a0`;
log SHA256 `03d3ce1ddc01520ddc3876be7c9ce12a1ee4bd950386ca385bc651e608b85687`.

Recovery changes only loader dispatch and adds a source-level assertion. No scientific
condition changes. The authoring protocol now also requires parent artifact/schema/loader
dispatch audits before presenting future C numbers as runnable.

Retry SAME C192; C193 remains unregistered.

## Active C192

One question:
Does frozen C181, as a read-only diagnostic shadow probe, predict SUFFICIENT on the actual
post3 fully observed states where runtime internal_remaining is already0?

No budget increase. No scheduler debit. No action. No state mutation.
Same C191 live path is replayed first.

Shadow cohort:928/selector =8352 total.
Expected regression1533;77 modules.
Source pins121; protected paths331; artifacts5.
Manifest:
`1d103bf279bd123f7e8ada5a5094242424715da5ed3bc01adff9a1ec881d0b12`.

PASS would isolate the remaining operational boundary to scheduler budget rather than post3
semantic recognition. It would not make the shadow probe runtime-authoritative.

C193 remains unregistered until C192 judgment.
