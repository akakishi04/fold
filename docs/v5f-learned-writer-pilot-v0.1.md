# V5-F learned semantic Writer pilot v0.1

C218 introduces the third learned memory component after accepted C216 Reader and C217 Port
Selector pilots.

## Scientific question

Given a structured observation descriptor, can a learned Writer choose the correct **factor +
relation** on a held-out nuisance combination, such that oracle ASSERT/REPLACE operation kind,
accepted H1/H2 memory semantics, frozen C217 Port Selectors and frozen C216 Readers preserve the
correct semantic answer?

## Changed variable

Only:

`fold_lm/v05/memory_writer.py`

is learned.

Model:

```text
observation descriptor [5]
  -> Linear(5,12)
  -> GELU
  -> Linear(12,6)
  -> factor+relation class
```

150 trainable parameters.

Six classes:

```text
alpha-class-0  alpha-class-1  alpha-class-2
beta-class-0   beta-class-1   beta-class-2
```

The Writer does **not** predict:
- operation kind;
- revision;
- scope authorization;
- evidence time.

ASSERT/REPLACE operation kind remains oracle so Writer semantic/factor learning is isolated.

## Observation dataset

Descriptor:

```text
alpha = [1,0,semantic,n1,n2]
beta  = [0,1,semantic,n1,n2]
semantic in {-1,0,+1}
```

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

Rows:

```text
2 factors * 3 semantic values * 4 nuisance states = 24
TRAIN = 18
EVAL  = 6
```

Every one of the six relation classes has exactly3 TRAIN rows and1 EVAL row.

Writer dataset SHA256:

`06f8df444119f0332168a956e7f32e9690b88fa9c39749d3ecc2283c70213714`

### Input-necessity controls

Factor-blind control zeros the first two factor-role channels. For each semantic value the alpha and
beta EVAL rows then become identical. Registered accuracy:

```text
factor-blind EVAL accuracy = 1/2
```

Semantic-blind control zeros the semantic scalar. For each factor the three semantic EVAL rows then
become identical. Registered accuracy:

```text
semantic-blind EVAL accuracy = 1/3
```

## Frozen downstream components

C217 selector checkpoint artifact:

`ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215`

C216 Reader checkpoint artifact inherited through C217 protected inputs:

`bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af`

All three C217 selectors and all three C216 Readers are restored and fingerprint-checked. Their
training steps are0 in C218.

## ASSERT integration

For every Writer seed, use the six unequal semantic pairs:

```text
(0,1) (0,2)
(1,0) (1,2)
(2,0) (2,1)
```

The Writer predicts alpha and beta factor+relation classes from EVAL observations. Those predictions
are used directly to construct ASSERT MemoryOps. Operation kind is oracle.

Each pair is read:
- while beta remains HOT;
- after beta is COMMITTED;
- for alpha query;
- for beta query.

This yields24 ASSERT rows per Writer seed.

Across every frozen selector × frozen Reader combination:

```text
ASSERT overall accuracy     1.0
ASSERT HOT accuracy         1.0
ASSERT COMMITTED accuracy   1.0
placement mismatches        0
write rejections            0
```

## REPLACE integration

For each of the six factor+relation target classes:

1. build an oracle initial state whose target factor holds a different semantic value;
2. use oracle REPLACE operation kind;
3. use the learned Writer prediction for factor+relation;
4. query the intended target factor through frozen Selector/Reader.

Six REPLACE rows per Writer seed.

Registered downstream accuracy:

```text
REPLACE accuracy = 1.0
```

If the Writer selects the wrong factor, the intended factor remains stale. If it selects the wrong
semantic relation, the intended factor contains the wrong value. Both therefore affect the final
answer.

## Negative controls

Two deterministic REPLACE controls are evaluated through all frozen Selector/Reader combinations:

- force the correct factor but wrong semantic relation;
- force the wrong factor.

Both require:

```text
downstream accuracy = 0.0
```

## Training

Writer seeds:

```text
218001
218002
218003
```

Per seed:
- Adam;
- lr0.02;
- betas0.9/0.999;
- eps1e-8;
- weight decay0;
-400 full-batch steps;
- batch18;
- CPU float32;
- threads2;
- deterministic algorithms.

Totals:

```text
trained Writer models       3
training steps           1200
training examples       21600
Writer forward calls      1212
frozen Selector forwards     3
frozen Reader forwards      72
total model forwards       1287
```

Execution schedule:

```text
learned Writer op slots      54
oracle initialization writes 60
control writes               12
chunk-commit slots           96
```

Successful learned writes/commits are measured separately from their scheduled slot counts so a
Writer prediction error becomes a scientific FAIL rather than an execution INVALID.

## Fixed PASS gate

Every Writer seed:
- TRAIN relation accuracy1.0;
- EVAL relation accuracy1.0;
- factor-blind EVAL accuracy0.5;
- semantic-blind EVAL accuracy1/3;
- checkpoint roundtrip exact;
- write rejections0;
- ASSERT overall/HOT/COMMITTED downstream accuracy1.0;
- ASSERT placement mismatches0;
- REPLACE downstream accuracy1.0.

Global controls:
- forced wrong-semantic accuracy0.0;
- forced wrong-factor accuracy0.0;
- frozen Selector/Reader fingerprints unchanged;
- actual learned Writer op attempts54/54;
- successful chunk commits96/96.

## Interpretation boundary

PASS means only that this small structured-observation Writer can learn factor+relation selection
and drive ASSERT/REPLACE through the accepted memory path while frozen learned Selector/Reader
components preserve the expected semantic output.

PASS does not establish:
- learned operation-kind selection;
- RETRACT/ASSUME writing;
- learned Coverage classifier;
- natural-language memory extraction;
- end-to-end Writer/Reader/Selector joint training;
- memory-cost advantage;
- Gate F.

C219 remains unregistered until C218 is formally judged.
