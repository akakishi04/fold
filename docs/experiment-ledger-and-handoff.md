# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C208 ACCEPTED VALID NEGATIVE. C209 ACTIVE / NOT YET JUDGED. C210 NOT REGISTERED.**

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
- model forward0
- scorer usedFalse
- adapter usedFalse
- header-compatible16
- target-status-compatible112
- necessity-compatible16
- target-compatible16
- combined-compatible16
- incompatible128
- only sufficient_reasoning_hard16/16 compatible
- every other family0/16
- candidate_gate_passed False

Accepted claim: the current frozen C181/C188 candidate input interface does not consume the fixed
C207 development schema as-is. The dominant blocker is the legacy7-node/4-fact shape; C188 also
rejects stale/conflict statuses when shape is otherwise legal.

## Active C209

Experiment:
`C209-v5e-visible-only-candidate-projection`

Stage:
`V5-E-VISIBLE-ONLY-CANDIDATE-PROJECTION`

One question:
can a deterministic visible-only candidate projection make all144 frozen C207 packets legal for
the current C181/C188 input contract while preserving Boolean semantics, original fact indices and
trusted runtime/evidence state?

Intervention:
- original fact order/indices unchanged;
- OBSERVED originals preserved exactly;
- every other original status becomes UNOBSERVED only in model projection;
- append OBSERVED TRUE architectural constants until4 facts;
- append `old_root AND TRUE` per dummy until7 nodes;
- dummy facts map to no original fact and must never be missing/selectable;
- original structured-v2 packet remains trusted and unchanged.

Registered totals:

```text
episodes144
original facts: 1->16, 2->112, 4->16
dummy TRUE facts272
status normalizations32
exhaustive semantic assignments736
semantic errors required0
equal source units50
equal projected units50
pair projection errors0
```

Required candidate-contract totals:

```text
C178 necessity-compatible144
C188 target-compatible144
combined-compatible144
dummy-missing errors0
```

Required purity totals:

```text
source unchanged144
source digest match144
mapping valid144
observed originals preserved144
nonobserved normalized safely144
dummy contract valid144
scorer_used False
trusted_runtime_mutated False
model_forward_calls0
```

Scope:
- candidate interface projection addedTrue
- no learned forward
- no candidate quality measurement
- baseline measurementFalse
- training0
- fresh seeds0
- network0
- production runtime modifiedFalse
- Gate E candidateFalse

Authoring:
- source pins77
- protected inputs149
- artifacts5
- new tests24
- regression modules94
- focused regression1973
- manifest
  `c6faab8b8b74fdf6b15dc7dbe3481def184e0dbdb04859a0b9e9ff90660b3879`

## Post-authoring review

**post_authoring_review = PASS**

review HEAD:
`1ad5adabf83307bf492ddeeaca03a40fb4ba0cf1`

Committed remote review verified accepted-valid-negative C208 identity and all6 C208 OWN blobs,
frozen C207 visible identity, projection module imports only standard library + structured-v1/v2,
no scorer/benchmark dependency in the projection API, original fact-index/status transformation
rules, TRUE-padding/AND wrappers, source-packet immutability,736 exhaustive semantic checks,
50 equal-source-unit preservation, actual C178/C188 validator calls, 24 C209 tests,
semantic1974-loaded/1973-kept regression accounting, zero unbound executable c### aliases across
projection/benchmark/tests, runner CLI indexes, dispatcher->launcher->runner PowerShell parser
chain, 77 source pins /149 protected inputs /5 artifacts, and C210 non-registration.

## Stop condition

Judge C209 before any C210 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/parent/regression/incomplete/protection failure -> INVALID / RETRY SAME C209.

Gate E remains NOT PASSED.
