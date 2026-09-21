# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C207 ACCEPTED PASS. C208 ACTIVE / NOT YET JUDGED. C209 NOT REGISTERED.**

## Accepted C207

Scientific execution HEAD:
`96020d20bd73bf6e2e62d5bfb202b7b2605a2079`

Published log commit:
`383033f391b65095011f3464f2c331c996706955`

Log SHA256:
`ab28e9961c6b1f07c6fdd1e7f3c72df021b89f4babb3182583e7a6f9caecefd0`

Summary SHA256:
`a7e69871003ac1978e786809c822d75c0dc291cfbe14aa8709f8b12ec26e4477`

Frozen development artifacts:
- visible `c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543`
- scorer `0591682848a69ac020a0f4a7bb2939e6df79ffd116567fe3c994a5f8e3fa3912`
- units `cb41d550651cb2dbb79f379bb0b6adb696914ecace02dc58cb1371f4e5a8deae`

C207 deciding result:
- focused regression **1929/1929**
-144 episodes /72 dependence units /144 roundtrips
- all9 families16 episodes each
- exact registered fault/action/channel counts
- answerable_with_budget128
- all validation/leakage/pair/payload errors0
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: a balanced leakage-free nine-family development-data boundary exists in the current
structured-v1/v2 schemas. Candidate/baseline performance and independent holdout are not measured.

## Active C208

Experiment:
`C208-v5e-candidate-input-compatibility-preflight`

Stage:
`V5-E-CANDIDATE-INPUT-COMPATIBILITY-PREFLIGHT`

One question:
can the current frozen C181/C188 candidate inference interface consume all144 frozen C207 visible
development packets as-is, without representation adaptation, scorer leakage or schema
reinterpretation?

Frozen input:
- C207 visible SHA
  `c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543`

Pinned current candidate input-contract sources:
- C178 blob `2ec87851f1f75533dd2225243d0c1baeda9c9a2a`
- C188 blob `0819bc70377a949fe1c17a66be559336bbda96e1`

C208 runs no model forward and does not load the C207 scorer artifact.

Per case C208 records:
- 7-node/4-fact header compatibility;
- active fact-slot count;
- active FACT-leaf count;
- C188 status compatibility;
- actual C178 validator acceptance/rejection;
- actual C188 validator acceptance/rejection;
- combined as-is compatibility.

Scientific PASS requires all144 rows combined-compatible.

Any complete valid result with incompatible rows is a scientific FAIL eligible for
**ACCEPTED VALID NEGATIVE**; incompatibility is not execution invalidity.

Scope:
- model forward0
- candidate measurementFalse
- baseline measurementFalse
- adapter implementationFalse
- training0
- fresh seeds0
- network0
- production runtime modifiedFalse
- Gate E candidateFalse

Authoring:
- source pins70
- protected inputs136
- artifacts5
- new tests20
- regression modules93
- focused regression1949
- manifest
  `52533ba9b2057f791b55cb6d1bafebf2cedfeae0400b5ecbf0f6a661ed77e7d6`

## Post-authoring review

**post_authoring_review = PASS**

review HEAD:
`1d115cc4e8ff9e2199388bf0108f3d11b1c72b7a`

Committed remote review verified accepted C207 summary/visible identity and all6 C207 OWN blobs,
exact C178/C188 source blobs, no scorer artifact load, no model forward or adapter path, expected
validator ValueError classification without broad exception swallowing, scientific PASS separated
from execution validity, 20 C208 tests, semantic1950-loaded/1949-kept regression accounting, zero
unbound executable c### aliases in benchmark/tests, runner CLI indexes, dispatcher->launcher->runner
PowerShell parser chain, 70 source pins /136 protected inputs /5 artifacts, and C209 non-registration.

## Stop condition

Judge C208 before any C209 registration.

- valid complete all-compatible result -> ACCEPTED PASS;
- valid complete incompatibility -> ACCEPTED VALID NEGATIVE;
- source/schema/parent/regression/incomplete/protection failure -> INVALID / RETRY SAME C208.

Gate E remains NOT PASSED.
