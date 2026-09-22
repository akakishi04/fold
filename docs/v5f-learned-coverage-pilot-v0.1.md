# V5-F learned Coverage classifier pilot v0.1

C219 introduces the fourth learned memory component after accepted Reader, Port Selector and
semantic Writer pilots.

## Scientific question

Can a learned Coverage classifier distinguish target-specific memory state as:

```text
SUPPORTED
HOT_REQUIRED
MISSING
OUT_OF_SCOPE
```

on a held-out nuisance combination, while preserving readable-path semantics through frozen
accepted C217 Port Selectors and C216 Readers?

`NUMERIC_UNSAFE` is intentionally excluded. It remains a deterministic numeric-safety status,
not an information-coverage class.

## Changed variable

Only:

`fold_lm/v05/memory_coverage.py`

is learned.

Classifier:

```text
coverage summary [7]
  -> Linear(7,12)
  -> GELU
  -> Linear(12,4)
```

148 trainable parameters.

## Bounded input summary

```text
[
  query_alpha,
  query_beta,
  target_in_H2,
  target_in_H1_hot,
  scope_live,
  nuisance_1,
  nuisance_2
]
```

The state summary is target-specific and bounded. It does not contain the full memory history,
numeric capsule readout, semantic answer, Writer target or future evidence.

Teacher semantics:

```text
scope_live = 0                  -> OUT_OF_SCOPE
target_in_H1_hot = 1           -> HOT_REQUIRED
target_in_H2 = 1               -> SUPPORTED
otherwise                      -> MISSING
```

## Dataset

Queries:
- alpha in `scope-alpha`;
- beta in `scope-beta`.

Both scopes are non-global so OUT_OF_SCOPE can be represented symmetrically.

TRAIN nuisance:

```text
[-1,-1]
[-1,+1]
[+1,-1]
```

EVAL nuisance:

```text
[+1,+1]
```

For both query roles and all four coverage classes:

```text
2 queries * 4 classes * 4 nuisance states = 32 rows
TRAIN = 24
EVAL  = 8
```

Class counts:

```text
TRAIN [6,6,6,6]
EVAL  [2,2,2,2]
```

Dataset SHA256:

`3e9c74b7675439c3118f6a87bc7594455360512e906d69c1c739cae9edc34d65`

## Necessity controls

### State-blind

Zero:

```text
target_in_H2
target_in_H1_hot
scope_live
```

All four classes collapse within each query role.

Registered EVAL accuracy:

```text
0.25
```

### Tier-blind readable

Evaluate only SUPPORTED/HOT_REQUIRED and zero:

```text
target_in_H2
target_in_H1_hot
```

Both readable states collapse onto the MISSING-shaped target summary.

Registered accuracy:

```text
0.0
```

### Scope-blind MISSING/OOS

Evaluate only MISSING/OUT_OF_SCOPE and zero:

```text
scope_live
```

The two classes become identical for each query role.

Registered accuracy:

```text
0.5
```

## Frozen readable reference

The accepted C217 selector checkpoint and accepted C216 Reader checkpoint are restored from the C218
protected-input chain.

For the four readable EVAL states:

```text
alpha SUPPORTED
alpha HOT_REQUIRED
beta  SUPPORTED
beta  HOT_REQUIRED
```

all 3 selector checkpoints × all 3 Reader checkpoints must produce semantic-answer accuracy1.0.

Frozen workload:

```text
selector forward calls 3
Reader forward calls   9
```

MISSING and OUT_OF_SCOPE rows are classification/gating cases and are not sent through the
readable reference path.

## Training

Coverage seeds:

```text
219001
219002
219003
```

Per seed:
- Adam;
- lr0.02;
- betas0.9/0.999;
- eps1e-8;
- weight decay0;
-400 full-batch steps;
- batch24;
- CPU float32;
- threads2;
- deterministic algorithms.

Total:

```text
coverage models            3
parameters/model         148
training steps          1200
training examples      28800
Coverage forward calls   1215
frozen Selector forwards    3
frozen Reader forwards      9
total model forwards      1227
```

Writer/Selector/Reader training steps are0.

## Fixed PASS gate

Every Coverage seed:

```text
TRAIN accuracy                         1.0
EVAL accuracy                          1.0
state-blind EVAL                       0.25
tier-blind readable                    0.0
scope-blind MISSING/OOS                0.5
readable gate accuracy                 1.0
non-readable suppression accuracy      1.0
MISSING <-> OUT_OF_SCOPE confusions    0
checkpoint roundtrip                   true
```

Global:
- frozen readable semantic reference accuracy1.0;
- all selector/reader fingerprints unchanged;
- NUMERIC_UNSAFE classified rows0.

## Interpretation boundary

PASS means only that this small classifier can learn the registered target-specific coverage
taxonomy, including explicit MISSING versus OUT_OF_SCOPE separation, from bounded structured runtime
state.

PASS does not establish:
- numeric-safety classification;
- natural-language coverage reasoning;
- joint Writer/Selector/Reader/Coverage training;
- information-acquisition integration;
- memory-cost advantage;
- Gate F.

C220 remains unregistered until C219 is formally judged.
