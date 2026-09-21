# C208 acceptance / C209 handoff

## Formal judgment

**C208 — ACCEPTED VALID NEGATIVE.**
**C209 NOT REGISTERED at this acceptance boundary.**
Gate E remains **NOT PASSED**.

Successful valid C208:
- scientific execution HEAD: `60d7b38bd0d44662f58b55b32cb09c4d9472f8fe`
- published log commit: `6af53ba7a905f0f9f216dc175dfa1273222ad198`
- log SHA256: `6a8e176dfb5af2607bd59c9481a454c7c3c207a4f96edfbf90f88facfdfbfba1`
- summary: `runs/c208-v5e-candidate-input-compat-cc0e510e762840c98f3d7cbb2b194652/summary.json`
- summary SHA256: `413e88c73c9f7af5403f8f4afa13d9b9245d3201788c41bb5713abc6d7125dc4`
- focused regression: **1949/1949** in 65.477s
- run_execution_valid True
- protected inputs preserved; tracked tree clean; execution HEAD preserved
- model forward calls0
- scorer usedFalse
- adapter usedFalse

## Deciding evidence

- episodes144
- classified rows144
- unexpected errors0
- header-compatible16
- target-status-compatible112
- necessity-compatible16
- target-compatible16
- combined-compatible16
- incompatible128

Per-family combined compatibility:
- sufficient_reasoning_hard16/16
- every other registered family0/16

Necessity rejection:
- `This diagnostic accepts exactly seven nodes and four facts`:128

Target rejection:
- `All four fact slots required`:128

Therefore:
- scientific_status FAIL
- candidate_gate_passed False
- diagnostic_execution_valid True

## Scientific interpretation

The current frozen C181/C188 candidate interface is not a general consumer of the C207 structured
Gate-E development schema. The dominant measured blocker is structural: only the16 four-fact,
seven-node reasoning-hard cases are accepted as-is.

A separate synthetic four-fact stale control also confirms that, once shape is legal, C188's target
contract additionally rejects non-UNOBSERVED/OBSERVED status values. That status limitation is
therefore real but masked by the larger shape incompatibility in the frozen C207 cohort.

This valid negative is retained. Families are not removed and C207 is not narrowed to fit the old
candidate interface.

## Next boundary

C209 should isolate one intervention question:

> Can a deterministic visible-only candidate projection transform every frozen C207 structured-v2
> packet into the legacy C181/C188 7-node/4-fact model-input contract while preserving Boolean
> semantics for every completion, preserving original fact indices, never exposing scorer data,
> never mutating runtime/evidence state, and making synthetic padding facts impossible acquisition
> targets?

Registered projection idea:
- keep original fact indices/order;
- any non-OBSERVED original fact becomes UNOBSERVED only in the model projection, with no payload or
  reference; original runtime status/reference remains outside and unchanged;
- append OBSERVED TRUE architectural constant facts until there are exactly4 facts;
- wrap the original expression root with `AND TRUE` once per appended fact, yielding exactly7 nodes
  while preserving the Boolean function;
- dummy facts declare no acquisition channel and are OBSERVED, so C188 never marks them missing;
- candidate projection is model-input only and cannot be used as the trusted runtime/evidence state.

C209 should perform no model forward. It tests projection feasibility/semantics only.
