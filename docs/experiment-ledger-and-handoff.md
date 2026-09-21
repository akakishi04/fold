# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, historical
> regression immutability, semantic count contracts, and Python import-binding audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C210 ACCEPTED PASS. C211 NOT REGISTERED.**

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

## Next boundary

C211 is not yet registered.

Next one-question intervention:

> Can the complete deciding Gate E manifest be frozen now, using only accepted development evidence,
> without evaluating the deciding holdout?

Candidate identity rule:
- verify all9 C210 candidate full summaries and full family summaries are identical;
- lexicographic tie-break selects
  `CANDIDATE-181001-188001`;
- base checkpoint SHA256
  `3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289`;
- selector checkpoint SHA256
  `02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d`.

C211 must freeze:
- independent144-episode /72-unit nine-family holdout with semantic templates not present in C207;
- exact visible/scorer/unit hashes;
- candidate/baseline identities;
- output schema and shared symbolic-answer disclosure;
- source/fault/budget schedule;
- hard-zero runtime/safety rules;
- zero-loss noninferiority versus FIXED_ACQUISITION on useful resolution/coverage/wrong abstention/
  unnecessary acquisition/user turns;
- +1-episode minimum strict improvement versus INTERNAL_ONLY on useful correct resolution and
  acquisition gain;
- one-sided exact paired McNemar tests for those two improvement claims, Holm familywise alpha0.05;
- per-family no-worse-than-fixed rules;
- unsupported-assertion floor rule: guarded candidate must remain0; strict reduction against the
  already-zero guarded internal baseline is explicitly not demonstrated;
- stop/invalidity rules.

C211 performs no model/baseline forward and no deciding holdout evaluation. Only after C211
acceptance may a later C execute the frozen holdout once.

Gate E remains NOT PASSED.
