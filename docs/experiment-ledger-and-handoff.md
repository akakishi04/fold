# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C192 ACCEPTED PASS. C193 NOT REGISTERED at this acceptance commit.**

C192 execution HEAD:
`583e7be99b3837690948634d9c8fc89967a5f573`
C192 published log commit:
`818738c1e4e06ea05f10f3f15e2413c92088fb63`
C192 summary SHA:
`05d1b0b7783ca8c3e0313a32172f8f7068ec0c9542042e7cfe2246bb81446ee1`.

C192: 1533/1533;85824 parent episodes replayed; shadow rows8352;
shadow/logical/nonfinite/mutation/read-after-shadow errors all0; run validTrue.

Claim:
frozen C181 recognizes every actual fully observed C191 post3 state as SUFFICIENT when read
diagnostically without mutating runtime. Remaining C191 blocker is explicit scheduler budget.

## Next design

C193 one question:
with only initial internal budget changed 12->13, does the full authoritative frozen learned
runtime remain correct and execute the final post3 necessity decision, ending SUFFICIENT?

Because internal_remaining is model-visible, C193 evaluates the whole budget13 path rather
than assuming C191/C192 intermediate predictions remain unchanged.

No training/fresh seeds/checkpoint/source/tool/provider changes.
C194 remains unregistered until C193 judgment.
