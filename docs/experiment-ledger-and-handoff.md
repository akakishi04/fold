# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> and post-authoring review pass apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C202 ACCEPTED PASS. C203 NOT REGISTERED.**

## Accepted C202

Scientific execution HEAD:
`a140f33b02aa4056b7c1fcff9041b09f9b7342c4`

Published log commit:
`bdf66220a633c8e3f261e09b7491369aec7f1994`

Log SHA256:
`b8b3e1f8663f606e1518be448983bc7855d656b265e228dc0dd23726cb37c640`

Summary SHA256:
`b568d8b652802c16fb75b85416c6d4ed956abcf767164d688ee39be1178e8c82`

C202 deciding result:
- focused regression **1785/1785**
- dispatch cases257472
- 27/27 block/channel records failed0
- provider calls257472
- publications257472
- receipts257472
- RETRIEVE/OBSERVE/ASK_USER provider calls85824 each
- route/action/dispatch/channel/receipt/value/mutation/resource errors0
- candidate_gate_passed True
- run_execution_valid True
- training/learned-forward/network0
- production runtime modified False

Accepted claim: each accepted learned target can execute through its exactly-one typed
RETRIEVE/OBSERVE/ASK_USER channel using the real structured acquisition lifecycle, with matching
provider isolation and exact selected-fact publication/resource semantics.

## Next boundary

C203 is not yet registered.

Next one-question intervention:
replay the full accepted C199 ALLOWED multi-step necessity/target trace while assigning different
semantic channels to different fact identities:

```text
fact0 -> RETRIEVE
fact1 -> OBSERVE
fact2 -> ASK_USER
fact3 -> RETRIEVE
```

Before each replayed learned decision, restore the accepted parent RETRIEVE-only runtime masks.
After NEEDS+target, trusted scheduler temporarily enables all three channels, maps the selected fact
through C201, dispatches through the C202 lifecycle, then restores parent masks before the next
replayed decision.

The expected acquisition depth, per-channel call totals and within-episode channel-switch count
must be derived only from the frozen accepted C199 prediction artifact and the fixed layout.

C203 must pass authoring quality gate and post-authoring remote-byte review before execution.

Gate E remains NOT PASSED.
