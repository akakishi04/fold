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

C203 remains **INVALID EXECUTION / RETRY SAME C203**. No C203 scientific result exists yet.

### Invalid attempt 1

- execution HEAD: `13b1db0c595f6d4900a038693f6c0d87728e3996`
- published log commit: `c437165ea115592fa6449791b62419f5ce0bb4ad`
- failure: 1812/1813 regression; source-audit test targeted wrong caller/callee namespace.
- scientific diagnostic not started.

### Invalid attempt 2

- execution HEAD: `fad0c9df501e38159dfe77b746c63456534024c4`
- published log commit: `529c081e898eb75a68eccf99113c49ff7aa6b681`
- log SHA256: `11bca2741e2d5a36dd9ebd2e834307f057babb7fca65b00405d35f69727d1277`
- focused regression: **1813/1813 PASS**
- failure occurred before block1/provider execution in parent-artifact projection;
- provider calls/publications0;
- run_execution_valid False.

Root cause:
C203 counted all nonnegative C199 target-head outputs as acquisitions. C199 writer stores a target
output for active rows whenever any row in the active batch still has missing facts, before checking
that row's necessity decision. A terminal SUFFICIENT row may therefore have a stored but unused
target prediction.

Recovery:
- acquisition depth now comes from `necessity == NEEDS(1)`;
- terminal SUFFICIENT target-head output is ignored;
- every NEEDS phase must have a valid corresponding target;
- final reference acquisition count is the NEEDS count;
- unit fixture now reproduces C199 terminal-target writer semantics.

Fixed parent totals remain:
- decisions214948;
- acquisitions129124;
- final SUFFICIENT85824.

Scientific manifest, fixed channel layout, parent identities, gate and workload are unchanged.

## Post-authoring review

**post_authoring_review = PENDING**

The revised review must now include:
- exact source-string assertion checks;
- C199 writer-side artifact semantics;
- parent gating semantics (stored target != executed acquisition);
- budget13/make_views identity reconstruction;
- authority grant/restore ordering;
- runner/launcher/manifest/count contracts.

Do not issue the next retry command until this review passes.

## Stop condition

Retry same C203 only after revised post-authoring review PASS.

C204 remains unregistered.
