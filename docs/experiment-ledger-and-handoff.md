# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2) and Experiment authoring quality gate apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\asobiba\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C192 ACCEPTED PASS. C193 ACTIVE / NOT YET JUDGED. C194 NOT REGISTERED.**

C192 execution HEAD:
`583e7be99b3837690948634d9c8fc89967a5f573`
C192 acceptance commit:
`c7a577bb0b82ffaf78c81b1a973ab1c3a9409bc8`
C192 summary SHA:
`05d1b0b7783ca8c3e0313a32172f8f7068ec0c9542042e7cfe2246bb81446ee1`.

C192:1533/1533; shadow rows8352; shadow/logical/nonfinite/mutation/read-after-shadow
errors all0. Frozen C181 recognizes every actual post3 fully observed state as SUFFICIENT;
C191's remaining blocker was scheduler internal budget0.

## Active C193

One variable only:
initial `internal_remaining 12 -> 13`.

Because the resource coordinate is model-visible, the entire learned path is rerun and
rescored rather than forcing C191 prediction replay.

For three-acquisition paths expected authoritative resources:
`13/4/7 ->12/4/8 ->8/3/12 ->4/2/16 ->0/1/20`.

The final post3 necessity prediction is scheduler-authoritative and must be SUFFICIENT.

Same85824 coherent-world episodes /9 frozen selector pairs.
No training/fresh seeds/checkpoint/source/tool/provider changes.
Expected regression1557;78 modules.
Source pins126; protected paths342; artifacts4.
Manifest:
`c038222b91af95f557a39171c18ed75e791e32455d74556c771875b9c68a95b5`.

C194 remains unregistered until C193 judgment.
