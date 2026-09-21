# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, parent artifact semantic audit, and historical
> regression immutability apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C205 ACCEPTED PASS. C206 NOT REGISTERED.**

## Accepted C205

Scientific execution HEAD:
`c78b79e95b92552c032df05220868122398fd339`

Published log commit:
`fd05da86e40e81feb96a3e7b6011e9d229299176`

Log SHA256:
`1dd3973c15013fb95296fda482eebe52298377c56eee3a9a50c7c3b0ee260427`

Summary SHA256:
`2f60e87aa7158bf22e1a4f6b15904a4e66096a1db81a6477e0b398be87fc3c2b`

C205 deciding result:
- focused regression **1871/1871**
-9/9 attribution blocks completed
- canonical unique rows15912 / forward calls18 / cell calls126
- canonical max necessity logit delta **0.0**
- canonical max target logit delta **0.0**
- expanded direct rows85824 / forward calls90 / cell calls630
- expanded max necessity logit delta **5.0067901611328125e-06**
- expanded max target logit delta **5.7220458984375e-06**
- max C204 necessity-max match error **0.0**
- max C204 target-max match error **0.0**
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: C204's gate-breaking numeric replay maxima are fully reproduced by phase0
duplicate-expanded batching. Canonical unique structured-v2 phase0 inference reproduces C199 logits
exactly. C204 remains ACCEPTED VALID NEGATIVE under its original1e-6 whole-run gate.

## Next boundary

C206 is not yet registered.

Gate E contract still requires a derived-result output boundary with supporting references. A
logical conclusion must not be represented as an observed fact.

Next one-question intervention:

> After reconstructing the accepted mixed-channel terminal SUFFICIENT states, can every terminal
> Boolean conclusion be emitted through the production `structured_derived_result.verify` contract
> as `VERIFIED_DERIVED`, bound to exactly the actually observed supporting references, while
> verification leaves observations/resources unchanged and rejects the opposite conclusion?

C206 should:
- hold the accepted C203/C204 behavioral trajectory fixed using the accepted C199 saved decision trace;
- replay actual mixed-channel acquisition through C201/C202/C173;
- use C171's benchmark-only proof fixture only as a reference candidate producer;
- use production `structured_derived_result.verify` as the deciding checker;
- compare the candidate conclusion to the independent C171 completion evaluator;
- verify the opposite conclusion is rejected;
- verify derived verification never changes fact status/value/reference/resource state;
- add no training, new seed, language generation or final Gate E claim.

C206 must pass authoring quality gate, immutable historical regression handling, PowerShell parser
preflight and post-authoring remote-byte review before execution.

Gate E remains NOT PASSED.
