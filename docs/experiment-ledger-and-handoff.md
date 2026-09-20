# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> and post-authoring review pass apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C202 ACCEPTED PASS. C203 ACTIVE / INVALID ATTEMPT RECOVERY. C204 NOT REGISTERED.**

## Accepted C202

Scientific execution HEAD:
`a140f33b02aa4056b7c1fcff9041b09f9b7342c4`

Published log commit:
`bdf66220a633c8e3f261e09b7491369aec7f1994`

Summary SHA256:
`b568d8b652802c16fb75b85416c6d4ed956abcf767164d688ee39be1178e8c82`

Accepted claim: each accepted learned target can execute through its exactly-one typed channel using
the real structured acquisition lifecycle, with matching-provider isolation and exact selected-fact
publication/resource semantics.

## Active C203

Experiment:
`C203-v5e-mixed-channel-multistep-replay`

The first C203 attempt is **INVALID EXECUTION / RETRY SAME C203**.

Invalid execution HEAD:
`13b1db0c595f6d4900a038693f6c0d87728e3996`

Published invalid log commit:
`c437165ea115592fa6449791b62419f5ce0bb4ad`

Log SHA256:
`cb59ebfadd11bbee559861ce38dddca027af9b3c28e93e08da619a7d3a658371`

Failure:
- repository/syntax/source prechecks PASS;
- focused regression1813;
-1812 PASS /1 FAIL;
- scientific diagnostic did not start;
- run_execution_valid False.

Root cause:
test22 incorrectly required the caller string
`predictions["necessity_predictions"]`
inside `replay_block()`, even though replay_block receives already-sliced `necessity` and
`targets` parameters. The implementation path was correct; the source-audit assertion targeted
the wrong function namespace.

Recovery:
- test22 now checks parent artifact reads in `collect()`;
- checks callee usage in `replay_block()`;
- no scientific condition, parent identity, workload, manifest or gate changed.

## Post-authoring review

**post_authoring_review = PASS**

revised review HEAD:
`d7d79dc2b51a424f4c49b59244e2a7a27456ce29`

The revised review mechanically evaluated every C203 source-string assertion against the exact
function source it inspects, including caller/callee ownership, live-inference call guards,
decision/action ordering, parent artifact contracts, runner/launcher wiring and C204 non-registration.

## Stop condition

Retry same C203 only after revised post-authoring review PASS.

C204 remains unregistered.
