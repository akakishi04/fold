# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> and post-authoring review pass apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C200 ACCEPTED PASS. C201 NOT REGISTERED.**

## Accepted C200

Scientific execution HEAD:
`11181a355f13e7be2fda3957b9cdd45ad8868316`

Published log commit:
`2694d336c11b2f98d5e9f89ed5442d445ac1d45e`

Log SHA256:
`75b48cc324db807542b0cd03a65ac182c40ca6113fcf9ddd77303db958eba04d`

Summary SHA256:
`624889546c9b484003e3f2bc79c1d746de28ea168def13da1a2dc87fde73520e`

C200 deciding result:
- focused regression **1731/1731**
- mask roundtrips32
- runtime authority cross448
- hidden pairs12
- malformed rejected18
- roundtrip/runtime-cross failures0
- hidden packet mismatches0
- answer-changing hidden pairs6
- v1 width72 / v2 width84
- v1 prefix preserved True
- candidate_gate_passed True
- run_execution_valid True
- training/learned-forward/provider/network activity0
- production runtime modified False

The earlier C200 attempt at
`4334bf492fe4d98e22165bb785edf3bcc9def254`
remains INVALID execution only; it failed in a false-positive authoring regression before the
scientific diagnostic.

Accepted claim: structured-task-input-v2 adds fact-specific
RETRIEVE/OBSERVE/ASK_USER eligibility as a strict12-bit tail while preserving the canonical
v1 72-feature prefix and runtime authority separation.

## Next boundary

C201 is not yet registered.

Next one-question intervention:
combine an accepted learned fact target with an exactly-one declared v2 channel and produce a
typed action proposal for that same fact, while leaving runtime authorization entirely to the
existing structured action runtime.

Reference mapper contract:

```text
v2 view + trusted RuntimeState + selected fact_index
-> require view.base == state.view
-> require exactly one declared channel for selected fact
-> ActionProposal(action=<that channel>, fact_index=<same index>)
```

The mapper must not:
- inspect hidden values;
- infer necessity;
- change the selected fact;
- intersect away denied/unavailable channels;
- execute a provider;
- bypass action.step authority.

C201 should use accepted C199 learned target predictions as the target source and register
separate authority-cross controls for RETRIEVE/OBSERVE/ASK_USER.

C201 must pass authoring quality gate and post-authoring remote-byte review before execution.

Gate E remains NOT PASSED.
