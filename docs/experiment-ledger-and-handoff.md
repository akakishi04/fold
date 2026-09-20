# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, and parent artifact semantic audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C203 ACCEPTED PASS. C204 NOT REGISTERED.**

## Accepted C203

Scientific execution HEAD:
`293b440adfddcbda0a18fd66184768c27aff49a2`

Published log commit:
`618772f2736279ae6389bfc5e488d1eb7c6b2553`

Log SHA256:
`f995c62b78b8dd23d2f29244c3ef52e4ea5243cbea6f3fbf0dacb968126ce8c2`

Summary SHA256:
`5fb52a6f056eea1fcf2ff719a9fa8c9efa9cc0d941ea26f50fdceed4c2db56c2`

C203 deciding result:
- focused regression **1813/1813**
- episodes85824
- learned decisions214948
- acquisitions129124
- final SUFFICIENT85824
- RETRIEVE88918 / OBSERVE21252 / ASK_USER18954
- within-episode channel switches32564
- failures0
- projection errors0
- decision/target/route/action/dispatch/provider-channel/receipt/fact-update/resource/final-status errors0
- candidate_gate_passed True
- run_execution_valid True
- production runtime modified False

Accepted claim: the accepted C199 multi-step decision trace can execute through the fixed
fact-specific mixed-channel layout, including32564 within-episode channel switches, while preserving
parent decision/acquisition depth, exact provider routing, fact publication, resource accounting and
final SUFFICIENT closure.

## Next boundary

C204 is not yet registered.

Next one-question intervention:
replace only the saved necessity/target replay with **live frozen-model inference after every
mixed-channel observation**.

At each decision:
- restore parent RETRIEVE-only authority;
- charge decision;
- construct current structured-v2 packet;
- require v2[0:72] == canonical v1 packet exactly;
- feed only that72-feature prefix to the accepted frozen C181/C188 models;
- compare live necessity/target predictions and logits to the accepted C199 ALLOWED artifact;
- execute live NEEDS target through the unchanged fixed C203 fact->channel layout;
- restore parent authority and repeat.

C204 must use the accepted C181 INTERNAL_SEMANTICS bases and C188 selectors with their protected
checkpoint identities. No retraining, threshold repair or saved-decision substitution is allowed.

C204 must pass authoring quality gate, parent writer/consumer semantic audit and post-authoring
remote-byte review before execution.

Gate E remains NOT PASSED.
