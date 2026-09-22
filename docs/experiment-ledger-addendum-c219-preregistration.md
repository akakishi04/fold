# C219 preregistration — V5-F learned Coverage classifier pilot

**C218 ACCEPTED PASS. C219 ACTIVE / NOT YET JUDGED. C220 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## One scientific question

Can a learned Coverage classifier distinguish SUPPORTED / HOT_REQUIRED / MISSING / OUT_OF_SCOPE
from a bounded target-specific memory summary on held-out nuisance input?

NUMERIC_UNSAFE is explicitly excluded from the classifier taxonomy.

## Parent checkpoint

C218 scientific execution HEAD:
`ce5ae96f5fe3a08213ee41bffa17ba97c10bb368`

C218 summary SHA256:
`50ec397534901bb865731b615232c555cfcf0222571f42b09098eae77f49f021`

C218 validation artifact SHA256:
`a0b235393fe3cd267534ecaa6de7190b534eb59a5fb8b95b1de083b6b4563359`

Inherited C217 selector checkpoint SHA256:
`ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215`

Inherited C216 Reader checkpoint SHA256:
`bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af`

C219 validates accepted C218 summary/artifacts, all144 parent source pins and all156 inherited
protected inputs, then extends that checkpoint with C219 OWN files.

## Changed variable

Learned Coverage classifier only:
`fold_lm/v05/memory_coverage.py`.

Architecture7->12->4; parameters148.

Classes:
`SUPPORTED / HOT_REQUIRED / MISSING / OUT_OF_SCOPE`.

## Data

Bounded feature schema:

```text
query_alpha
query_beta
target_in_H2
target_in_H1_hot
scope_live
nuisance_1
nuisance_2
```

TRAIN nuisance:
`[-1,-1],[-1,+1],[+1,-1]`.

EVAL nuisance:
`[+1,+1]`.

32 rows /24 TRAIN /8 EVAL.

Each class:
- TRAIN6;
- EVAL2.

Coverage data SHA:
`3e9c74b7675439c3118f6a87bc7594455360512e906d69c1c739cae9edc34d65`.

## Fixed controls

```text
state-blind EVAL accuracy             0.25
tier-blind readable accuracy          0.0
scope-blind MISSING/OOS accuracy      0.5
```

The scope-blind control directly tests the evidence required to separate MISSING from OUT_OF_SCOPE.

## Frozen readable reference

Accepted C217 Selectors and C216 Readers are frozen.

Four readable EVAL rows are checked through all3x3 selector/Reader combinations.

Required:
- semantic reference accuracy1.0;
- selector forwards3;
- Reader forwards9;
- Selector/Reader training steps0.

Writer is not exercised in C219.

## Training

Seeds219001/219002/219003.

Adam lr0.02, betas0.9/0.999, eps1e-8, weight decay0,400 full-batch steps, batch24,
CPU float32, threads2, deterministic algorithms.

Registered workload:
- models3;
- parameters148;
- training steps1200;
- examples28800;
- Coverage forwards1215;
- frozen Selector forwards3;
- frozen Reader forwards9;
- total model forwards1227;
- Writer/Selector/Reader training0;
- network calls0.

## Fixed PASS gate

Every seed:
- TRAIN accuracy1.0;
- EVAL accuracy1.0;
- state-blind0.25;
- tier-blind readable0.0;
- scope-blind MISSING/OOS0.5;
- readable gate1.0;
- non-readable suppression1.0;
- MISSING/OOS confusions0;
- checkpoint roundtrip exact.

Global:
- readable frozen downstream reference1.0;
- frozen Selector/Reader roundtrips exact;
- NUMERIC_UNSAFE classified rows0.

Complete execution missing a gate = scientific FAIL.
Source/artifact/schema/regression defects = INVALID / RETRY SAME C219.

## Scope

Writer learning absent.
Selector/Reader frozen.
NUMERIC_UNSAFE deterministic and excluded.
No acquisition integration.
No Gate F decision.

## Authoring registration

OWN7:
- `fold_lm/v05/memory_coverage.py`
- `fold_lm/v05_benchmarks/gate_f_c219_learned_coverage.py`
- `tests_lm/test_v05_c219_learned_coverage.py`
- `tools/run_c219.ps1`
- `tools/invoke_c219.ps1`
- this preregistration
- `docs/v5f-learned-coverage-pilot-v0.1.md`

Expected:
- source pins151;
- protected inputs169;
- artifacts5;
- C219 tests38;
- regression modules104;
- loaded tests2298;
- exact historical exclusion1;
- focused regression2297.

Manifest SHA256:
`466ee5cd488a08ef9b8dacc6bf9f544ba4ca83ff2ab80dc2af421a6be9db43aa`

## Post-authoring review

`post_authoring_review = PASS`

review HEAD:
`bb52254ff6a1f7bf3b6195451a830cd498f533d4`

Committed remote review verified:
- accepted C218 execution/summary/validation identity;
- all144 C218 source blobs remain at their registered Git blob IDs;
- all156 inherited protected inputs remain registered;
- inherited C217 selector and C216 Reader checkpoints each resolve uniquely at the exact registered SHA;
- C219 OWN7 extends source pins to151 and protected inputs to169;
- all11 deciding-path repository dependencies are parent/OWN pinned;
- Coverage dataset SHA independently recomputes to
  `3e9c74b7675439c3118f6a87bc7594455360512e906d69c1c739cae9edc34d65`;
- manifest independently recomputes to
  `466ee5cd488a08ef9b8dacc6bf9f544ba4ca83ff2ab80dc2af421a6be9db43aa`;
- four-class taxonomy is exact and NUMERIC_UNSAFE is absent;
- MISSING and OUT_OF_SCOPE differ by scope_live in the target-specific summary;
- state/tier/scope blind controls are registered at0.25/0.0/0.5 and independently reproduced;
- readable reference uses actual bank reads for SUPPORTED/HOT_REQUIRED and frozen3x3 Selector/Reader combinations;
- non-readable classes are classification/gating cases and are excluded from the readable reference;
-38 C219 tests,104 regression modules,2298 loaded /2297 focused counts are exact;
- executable c### alias binding defects are0;
- runner argv ordering is precheck argv[1], postcheck argv[1..3];
- complete test37 PowerShell source contract is satisfied;
- C220 remains unregistered.

No scientific threshold, split, seed, model architecture or workload was changed after activation.

Do not issue C219 execution until committed remote bytes are independently reviewed for:
- accepted C218 summary/artifact identity;
- inherited Selector/Reader checkpoint resolution;
- all144 parent source pins and156 parent protected inputs;
-151/169 accounting;
- exact four-class taxonomy and NUMERIC_UNSAFE exclusion;
- dataset hash/split/class balance;
- state/tier/scope blind controls;
- MISSING versus OUT_OF_SCOPE semantics;
- frozen readable reference;
- fixed workload/manifest;
-38 tests /104 modules /2298->2297;
- free-name/import bindings;
- direct dependency coverage;
- runner CLI indexes;
- complete PowerShell source-string contract;
- C220 non-registration.
