# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C206 ACCEPTED PASS. C207 ACTIVE / NOT YET JUDGED. C208 NOT REGISTERED.**

## Accepted C206

Scientific execution HEAD:
`814dd2b51a1ff03011aeb609eae1cd75041f1428`

Published log commit:
`c3bc6823eac2dec8a08395f7ecf1f3d63229831f`

Log SHA256:
`0adfbba30f863864ca4e95a05fb3c3679f34db5cb2628d9a73b60bc5edefa112`

Summary SHA256:
`1fd274cc8d8686b7779838df2f62670da52ddeb87f01a026b4d96cbf62db7553`

C206 deciding result:
- focused regression **1901/1901**
-9/9 scientific blocks complete
- episodes85824
- decisions214948
- acquisitions129124
- terminal SUFFICIENT85824
- VERIFIED_DERIVED85824
- opposite controls rejected85824
- verifier calls171648
- RETRIEVE88918 / OBSERVE21252 / ASK_USER18954
- channel switches32564
- support_min1 / support_max4
- checked_steps328275
- all runtime/semantic/world/verifier/support/mutation/schema errors0
- failures0 / projection errors0
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: every registered mixed-channel terminal SUFFICIENT state emits through the
production bounded derived-result verifier as VERIFIED_DERIVED with only actually OBSERVED support;
the opposite conclusion is rejected; trusted observation/resource state remains unchanged.

## Active C207

Experiment:
`C207-v5e-nine-family-development-manifest`

Stage:
`V5-E-NINE-FAMILY-DEVELOPMENT-MANIFEST`

One question:
can all nine Gate E v0.1 families be represented in a fixed balanced development manifest using
only existing structured-v1/v2 schemas and runtime metadata, with paired dependence units and all
hidden completions / semantic conclusions / necessity/action labels / fault outcomes scorer-only?

Registered development split:
-9 families;
-8 dependence units per family;
-2 conditions per unit;
-16 episodes per family;
-72 dependence units;
-144 episodes;
-144 structured-v2 roundtrips;
-no independent holdout.

Visible artifact contains only case/unit/family/condition plus canonical structured-v2 packet.

Scorer artifact contains only evaluator-side:
- source value;
- semantic conclusion;
- answerable-with-budget;
- necessary/unnecessary facts;
- expected proposal/terminal;
- fault schedule.

Fixed counts:

```text
faults:
NONE128
MALFORMED_PAYLOAD8
MISSING_DELIVERY2
PERMISSION_DENIED3
BUDGET_EXHAUSTED3

expected proposals:
ANSWER48
RETRIEVE48
OBSERVE32
ASK_USER16

eligible-channel episodes:
RETRIEVE64
OBSERVE32
ASK_USER16

answerable_with_budget128
```

Required errors all0:
- duplicate case IDs
- family count
- unit
- visible schema
- scorer leakage
- pair
- scorer contract
- hidden payload

Scope:
- candidate measurementFalse
- baseline measurementFalse
- numerical margin registrationFalse
- training0
- fresh seeds0
- network0
- production runtime modifiedFalse
- Gate E candidateFalse

Authoring:
- source pins62
- protected inputs122
- artifacts5
- new tests28
- regression modules92
- focused regression1929
- manifest
  `d9d3ea599b19f1c7fa91af9e1d0a96287391ae8d4ea88b91449cb5ad4ff61f72`

Historical mutable-state regression exclusion remains one exact accepted C204 test ID.

## Post-authoring review

**post_authoring_review = PASS**

review HEAD:
`5d2115e39f3986513387281ec8de3f1723cbcfc1`

Committed remote review verified accepted C206 execution/source identity, all9 family names, balanced
144-episode /72-unit fixture counts, dependence-unit binding identity, visible/scorer separation,
non-OBSERVED no-payload checks, hidden-pair equality/difference contracts, exact fault/action/channel
counts, no candidate/baseline/holdout claim, 28 C207 tests, semantic1930-loaded/1929-kept regression
accounting, zero unbound executable c### aliases in benchmark/tests, runner/launcher argument wiring,
PowerShell parser chain, 62 source pins /122 protected inputs /5 artifacts, and C208 non-registration.

## Stop condition

Judge C207 before any C208 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/parent/regression/incomplete/protection failure -> INVALID / RETRY SAME C207.

Gate E remains NOT PASSED.
