# V5-F learned Port Selector pilot v0.1

C217 introduces the second learned memory component after accepted C216.

## Scientific question

Given correct H1/H2 memory and the three frozen accepted C216 Readers, can a learned Port Selector
choose the correct alpha/beta memory port from a query descriptor on a held-out nuisance
combination, such that downstream semantic answers match oracle routing?

## Changed variable

Only:

`fold_lm/v05/memory_port_selector.py`

is learned.

Model:

```text
query descriptor [4]
  -> Linear(4,8)
  -> GELU
  -> Linear(8,2)
  -> alpha/beta port
```

58 trainable parameters.

The selector never receives:
- memory values;
- Reader output;
- target semantic class;
- memory placement/status;
- scope/provenance.

## Held constant

- Writer: oracle/deterministic.
- Reader: all three accepted C216 Reader checkpoints frozen.
- Coverage classifier: absent.
- H1/H2 semantics: fixed.
- response-capsule algebra: fixed.
- no language mapping.

Frozen Reader checkpoint artifact:

`bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af`

Frozen Reader final fingerprints:
- seed216001: `6f1219b4277e3d4af6494ecf2280f2442887df05d5d133f2e2566b29bf804336`
- seed216002: `1b7b2f96ad3e33d4ac0422cd7ca72b7f6e53707acf52aa17a44f188b7c2ed199`
- seed216003: `3d26451e54a8e4327f2dcc9128e73c7e3fc60605c3e2d894876bd65057d2dd7f`

## Query dataset

Descriptor:

```text
alpha = [1,0,n1,n2]
beta  = [0,1,n1,n2]
```

TRAIN nuisance combinations:

```text
[-1,-1]
[-1,+1]
[+1,-1]
```

EVAL nuisance combination:

```text
[+1,+1]
```

Rows:
-8 total;
-6 TRAIN;
-2 EVAL;
- both ports balanced in both splits.

Query dataset SHA256:

`a9ec25d8079e27177567dd4ca85c7aee18f511eb8e8db6b774a61af82e91ac3d`

Query-blind control zeros the first two role channels on EVAL. Both rows then become identical, so
a deterministic selector can achieve exactly one correct prediction out of two:

```text
query-blind EVAL accuracy = 0.5
```

## Downstream memory fixture

Use only unequal semantic pairs:

```text
(0,1) (0,2)
(1,0) (1,2)
(2,0) (2,1)
```

For each pair:
- ASSERT+commit alpha;
- ASSERT beta;
- HOT read;
- commit beta;
- COMMITTED read;
- query both alpha and beta.

This yields:

```text
6 pairs * 2 placements * 2 queries = 24 downstream rows
```

Because alpha != beta for every row, selecting the wrong port must produce the other semantic class.
With frozen C216 Readers:

```text
correct-port downstream accuracy = 1.0
forced-wrong-port accuracy       = 0.0
```

for every selector seed × Reader checkpoint.

## Training

Selector seeds:

```text
217001
217002
217003
```

Per seed:
- Adam;
- lr0.02;
- betas0.9/0.999;
- eps1e-8;
- no weight decay;
-400 full-batch steps;
- batch6;
- CPU float32;
- threads2;
- deterministic algorithms.

Totals:
-3 selector models;
-1200 training steps;
-7200 training examples;
-1209 selector forward calls including scoring;
-18 frozen Reader forward calls;
-1227 total model forwards;
- Reader training steps0;
- oracle Writer operations12;
- chunk commits12.

## PASS gate

Every selector seed must independently satisfy:

```text
TRAIN port accuracy             1.0
EVAL port accuracy              1.0
query-blind EVAL accuracy       0.5
selector checkpoint roundtrip   true
```

For all three frozen Readers:

```text
downstream accuracy             1.0
HOT downstream accuracy         1.0
COMMITTED downstream accuracy   1.0
forced-wrong-port accuracy      0.0
placement mismatches            0
```

## Interpretation boundary

PASS means only that the tiny learned Port Selector can route a synthetic held-out query descriptor
to the correct two-port memory location and preserve the already-demonstrated Reader answer.

PASS does not establish:
- learned Writer;
- learned Coverage classifier;
- language query understanding;
- many-port scaling;
- memory cost advantage;
- Gate F.

C218 remains unregistered until C217 is formally judged.
