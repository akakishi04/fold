# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C210 ACCEPTED PASS. C211 ACTIVE / NOT YET JUDGED. C212 NOT REGISTERED.**

## Accepted C210

Scientific execution HEAD:
`002543b8d1394c127b915b3bfe4591ce20c8939d`

Published log commit:
`a04e7cdc5b42939e2d65f395f12da450a896bf0f`

Log SHA256:
`f1365f6d364c5bf0729ef7240f69c2c566004eef554a35c08b8b32355039f0d3`

Summary SHA256:
`1b4242f15fdf3ca48374660d5c3339ff5c17dc9cd4f4833852f5e1bccb349366`

C210 deciding result:
- focused regression **1997/1997**
- policy-episode evaluations1584
- measurement_complete True
- run_execution_valid True
- numerical margin registration False
- candidate selection False
- independent holdout created False

INTERNAL_ONLY:
- correct48 / answered48 / unresolved96
- attempts0 / provider calls0 / publications0 / user turns0
- wrong abstention80 / wrong answers0

FIXED_ACQUISITION:
- correct128 / answered128 / unresolved16
- attempts96 / provider calls90 / publications80 / user turns16
- wrong abstention0 / wrong answers0
- authority violations0 / malformed publications0

All9 candidate model pairs are identical in full policy and per-family summaries:
- correct128 / answered128 / unresolved16
- attempts96 / provider calls90 / publications80 / user turns16
- wrong abstention0 / wrong answers0
- unnecessary acquisition0 / missed necessary acquisition0
- premature sufficient0 / repeated NEEDS0 / invalid target0
- inference rows224 / forward calls2 / cell calls14

Accepted claim: the matched development measurement is complete. This acceptance refers to the
retry execution at `002543b8d1394c127b915b3bfe4591ce20c8939d`; the earlier unprotected attempt
remains invalid historical evidence. C210 does not itself select a candidate or register numerical
acceptance margins.

## Active C211

Experiment:
`C211-v5e-deciding-manifest-freeze`

Stage:
`V5-E-DECIDING-MANIFEST-FREEZE`

One question:
can the complete deciding Gate E registration be frozen from accepted development evidence without
evaluating the deciding holdout?

Frozen candidate:
`CANDIDATE-181001-188001`

Tie-break requires all9 C210 candidate full policy/family summaries to be exactly equal before
lexicographic selection.

Pinned checkpoint hashes:
- base `3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289`
- selector `02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d`

C211 creates a144-episode /72-unit independent nine-family deciding holdout with expression
signatures disjoint from C207 development, freezes exact artifact hashes and registers:
- zero-episode noninferiority margins versus FIXED_ACQUISITION;
- +1-episode strict improvement margins versus INTERNAL_ONLY for two primary claims;
- one-sided exact paired McNemar with Holm alpha0.05 across exactly2 claims;
- hard-zero runtime/safety rules;
- zero-floor unsupported-assertion limitation;
- candidate compute ceilings;
- stopping/invalidity rules.

C211 performs no holdout policy/model evaluation.

Authoring:
- source pins89
- protected inputs173
- artifacts5
- tests28
- regression modules96
- focused regression2025
- manifest `81e13c77066aa61f6487d341488812c00ad057fba97a30c31c62e9e2bc6fb859`

## Post-authoring review

**post_authoring_review = PENDING**

Do not issue C211 execution command until committed remote bytes are independently reviewed for
parent identity, candidate tie/checkpoints, holdout independence, decision rules, no-evaluation
boundary, regression counts, aliases, PowerShell parser chain and CLI indexes.

## Stop condition

Judge C211 before any C212 registration.

Gate E remains NOT PASSED.
