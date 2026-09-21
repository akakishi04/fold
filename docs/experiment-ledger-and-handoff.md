# FOLD Experiment Ledger and Handoff

> Authoritative current state. Current response format (v2), Experiment authoring quality gate,
> post-authoring review, PowerShell parser preflight, and parent artifact semantic audit apply.

Repository `akakishi04/fold`; branch `feat/sft-target-loss`; local `M:\\asobiba\\fold`.
Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5.

## Formal state

Gate A/B PASSED; C/D PASSED in measured scope; **Gate E NOT PASSED**.
**C204 ACCEPTED VALID NEGATIVE. C205 ACTIVE / INVALID ATTEMPT RECOVERY. C206 NOT REGISTERED.**

## Accepted C204

Scientific execution HEAD:
`0ef49a4f97b516a00066df4986c062f98fda676d`

Published log commit:
`df0a850ee298c643a7b775988cef69cd24b42655`

Log SHA256:
`f1c4db1a22d61b0ebfc09ff21937e500eefe6f43f1d198b3c2920fcc07c2b56a`

Summary SHA256:
`9c02e4dbd497fbc91ae25c02f4cc5a3baad0af8cf9cc296f2bac0f6f8ffe72e9`

Execution validity:
- focused regression **1846/1846**
- all9 live blocks completed
- run_execution_valid True
- protected inputs preserved
- tracked tree clean
- execution HEAD preserved
- production runtime modified False

Behavioral/runtime equivalence:
- episodes85824
- decisions214948
- acquisitions129124
- final SUFFICIENT85824
- v2 packets214948
- inference rows214948
- necessity prediction errors0
- target prediction errors0
- v2 prefix errors0
- RETRIEVE88918 / OBSERVE21252 / ASK_USER18954
- channel switches32564
- failures0 / projection errors0

Valid negative condition:
- max necessity logit delta `5.0067901611328125e-06`
- max target logit delta `5.7220458984375e-06`
- preregistered tolerance `1e-6`
- scientific_status FAIL
- candidate_gate_passed False

Accepted claim: live frozen inference from the exact72-feature prefix of structured-v2 reproduces
all accepted C199/C203 argmax decisions and runtime behavior, but not logits within the fixed1e-6
numeric replay tolerance.

## Active C205

Experiment:
`C205-v5e-phase0-batch-composition-attribution`

Stage:
`V5-E-PHASE0-BATCH-COMPOSITION-ATTRIBUTION`

One question:
are the C204 gate-breaking logit maxima fully attributable to phase0 duplicate-expanded batch
composition rather than structured-v2 prefix/state semantics?

Registered comparison:
- canonical unique:1768 unique phase0 states -> v2 prefix -> frozen inference -> expand by local_rows;
- expanded direct:9536 world-expanded duplicate phase0 states -> v2 prefix -> frozen inference directly.

Both use:
- same accepted C181/C188 checkpoints;
- BATCH1024;
- CPU float32;
- threads2;
- deterministic algorithms;
- raw argmax;
- same C199 phase0 reference;
- unchanged1e-6 tolerance.

Required canonical path:
- prefix errors0
- expanded-prefix mismatches0
- prediction errors0
- both max logit deltas <=1e-6

Required expanded path:
- prefix errors0
- prediction errors0
- both max logit deltas >1e-6
- each block max must reproduce the corresponding C204 whole-loop block max within1e-12

Registered workload:
- canonical rows15912 / forward calls18 / cell calls126
- expanded rows85824 / forward calls90 / cell calls630

Scope:
- training0
- fresh seeds0
- acquisitions0
- network0
- production runtime modifiedFalse
- Gate E candidateFalse

Authoring:
- expected regression **1871 =1846 inherited -1 exact mutable historical test +26 C205 tests**
- modules **90**
- source pins44
- protected inputs92
- artifacts5
- manifest
  `316f8ec5e4654a321aff67ddf48e067feb29cf786e330697230ad3187e6f8c0c`

## Invalid C205 attempt

Execution HEAD:
`37509d34e1ccfc8abf3e92fca708327a5335e4ea`

Published log commit:
`81346818971e8586dbd1629563f76a847c6e279a`

Log SHA256:
`e98725bfd5c20b9e612f3640cf931f86beb5c00618f1e92b1c9e77a5d10d420b`

- focused regression1871;
-1870 PASS /1 FAIL;
- failing test was accepted C204 test33 asserting current ACTIVE == C204;
- current ACTIVE correctly equals C205;
- all25 original C205 tests PASS;
- scientific diagnostic did not start;
- run_execution_valid False.

Recovery:
- accepted C204 files remain unchanged;
- C205 focused suite excludes exactly that one mutable historical test ID;
- C205 adds an immutable replacement test;
- total executed regression remains1871;
- scientific question/tolerance/workload/gate unchanged.

## Post-authoring review

**post_authoring_review = PASS**

recovery review HEAD:
`2bd2ec0424db21e8ed2bfa0c7be07f8148d69afa`

Committed remote review verified:
- accepted C204 test blob unchanged;
- one exact historical mutable-state test ID excluded with exact-once guard and no wildcard;
-1872 loaded candidates ->1871 executed regression tests;
-26 C205 immutable tests including the replacement contract;
- runner uses `regression_suite()`;
- C205 scientific question,1e-6 tolerance, workload and attribution gate unchanged;
- source pins44 / protected inputs92;
- dispatcher -> C205 launcher -> C205 runner parser guards precede execution/logging;
- C206 remains unregistered.

## Stop condition

Judge C205 before any C206 registration.

- valid complete gate pass -> ACCEPTED PASS;
- valid complete scientific miss -> ACCEPTED VALID NEGATIVE;
- source/schema/hash/checkpoint/reference/regression/incomplete/protection failure
  -> INVALID / RETRY SAME C205.

Gate E remains NOT PASSED.
