# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) applies.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C191 ACCEPTED PASS. C192 NOT REGISTERED at this acceptance commit.**

C191 scientific execution HEAD:
`f83ed1d60758dc1ff895b2b9c42c69d6a68c0931`
C191 published log commit:
`b034ac0a56117130dbbd837d5493ad27c29433d1`
C191 summary SHA:
`b05cd702e9572c61a3ae981e5279c7fb096fe1078c7d65f6401f180f307c84f4`.

C191: 1509/1509;85824 episodes; all scientific counters0;
third acquisitions8352; final logical NEEDS0; fourth decision accepted0;
initial replay deltas0.0; run validTrue.

Claim: unchanged budget12 supports three real acquisitions on the full C190 coherent-world
cohort, then reaches exact internal budget0 and correctly refuses a fourth scheduler decision.

Non-claim: no executable learned post3 reclassification.

## Next design

C192 one question:
on the actual C191 post3 fully observed state with internal_remaining0, does frozen C181
diagnostically predict SUFFICIENT without any scheduler debit/state mutation?

This is read-only semantic diagnosis, not a runtime-authoritative action.
No budget increase, no training, no fresh seed, no tool/provider change.
C193 remains unregistered until C192 judgment.
