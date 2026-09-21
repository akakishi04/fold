# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C208 ACCEPTED VALID NEGATIVE. C209 NOT REGISTERED.**

## Accepted C208

Scientific execution HEAD:
`60d7b38bd0d44662f58b55b32cb09c4d9472f8fe`

Published log commit:
`6af53ba7a905f0f9f216dc175dfa1273222ad198`

Log SHA256:
`6a8e176dfb5af2607bd59c9481a454c7c3c207a4f96edfbf90f88facfdfbfba1`

Summary SHA256:
`413e88c73c9f7af5403f8f4afa13d9b9245d3201788c41bb5713abc6d7125dc4`

C208 deciding result:
- focused regression **1949/1949**
- episodes144 / classified144
- run_execution_valid True
- model forward calls0
- scorer usedFalse
- adapter usedFalse
- header-compatible16
- target-status-compatible112
- necessity-compatible16
- target-compatible16
- combined-compatible16
- incompatible128
- only `sufficient_reasoning_hard` is16/16 compatible; every other family0/16
- necessity rejection `This diagnostic accepts exactly seven nodes and four facts`:128
- target rejection `All four fact slots required`:128
- candidate_gate_passed False

Accepted claim: the frozen C181/C188 candidate interface is narrower than the fixed C207
development schema. The dominant measured blocker is the legacy7-node/4-fact representation
contract. C188 additionally rejects non-UNOBSERVED/OBSERVED statuses once shape is legal.

## Next boundary

C209 is not yet registered.

Next one-question intervention:

> Can a deterministic visible-only model-input projection map every frozen C207 packet into the
> legacy7-node/4-fact C181/C188 contract while preserving Boolean semantics for every completion,
> preserving original fact indices, keeping synthetic padding facts unselectable for acquisition,
> never using scorer data, and never mutating trusted runtime/evidence state?

Registered projection concept:
- preserve original fact order/indices;
- normalize every non-OBSERVED original fact to UNOBSERVED only in the candidate projection;
- remove references from those normalized projection facts;
- append OBSERVED TRUE architectural constants until four facts exist;
- append `AND TRUE` wrappers around the original root until seven nodes exist;
- padding facts have no acquisition channel and remain OBSERVED;
- original C207 v2 packet remains the trusted runtime/evidence state and is unchanged;
- the projection is candidate-input-only.

C209 should perform no learned forward. It is projection-feasibility/semantics only.

Gate E remains NOT PASSED.
