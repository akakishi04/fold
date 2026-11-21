# V5-F learned Reader pilot v0.1

C216 introduces the first learned memory component after the accepted deterministic C213-C215
memory chain.

## Scientific question

Given a correct H1/H2 memory state and an **oracle-selected memory port**, can a learned Reader
decode the selected numeric FOLD-R readout into the correct three-way semantic value on held-out
alpha/beta value pairings, while remaining invariant to HOT versus COMMITTED placement?

## Changed variable

Only:

`fold_lm/v05/memory_reader.py`

is learned.

The model is:

```text
selected scalar port readout
  -> Linear(1,8)
  -> GELU
  -> Linear(8,3)
  -> semantic class {-1,0,+1}
```

43 trainable parameters.

## Held constant / oracle

- Writer: oracle/deterministic.
- Port Selector: oracle; query alpha -> port0, beta -> port1.
- Coverage classifier: absent.
- H1/H2 semantics: accepted C215 implementation.
- relation-to-port mapping: fixed.
- response-capsule algebra: fixed.
- no language parsing.
- no network access.

Query ID and memory status are **not Reader input features**.

## Dataset

Semantic values:

```text
class0 = -1
class1 =  0
class2 = +1
```

All 9 alpha/beta class pairs are constructed.

Held-out EVAL pairs:

```text
(alpha0,beta1)
(alpha1,beta2)
(alpha2,beta0)
```

The other six pairs are TRAIN.

Every marginal alpha value and every marginal beta value occurs in both TRAIN and EVAL. The split
therefore withholds pair composition, not the individual three scalar meanings.

For each pair:

1. ASSERT alpha;
2. commit alpha to H2;
3. ASSERT beta;
4. read HOT state;
5. commit beta;
6. read COMMITTED state;
7. oracle-select alpha port and beta port in both placements.

Rows:

```text
9 pairs * 2 placements * 2 queries = 36
TRAIN = 24
EVAL  = 12
```

Target distributions are exactly balanced:
- TRAIN: [8,8,8];
- EVAL: [4,4,4].

Dataset SHA256:

`9ded8a1b17cf721407e5d28c9dd6350159d0a17721f39bf9b57a911b78aa3f61`

## Training registration

Seeds:

```text
216001
216002
216003
```

Per seed:

```text
optimizer     Adam
lr            0.02
betas         0.9 / 0.999
eps           1e-8
weight decay  0
steps         400
batch         24 (entire TRAIN split)
dtype         float32
device        CPU
threads       2
deterministic algorithms enabled
```

Total:
- trained models3;
- training steps1200;
- examples drawn28800;
- Reader forward calls1215 including scoring.

## Fixed PASS gate

Every seed independently must satisfy:

```text
TRAIN accuracy       = 1.0
EVAL accuracy        = 1.0
EVAL HOT accuracy    = 1.0
EVAL COMMITTED acc   = 1.0
placement mismatches = 0
```

Readout-necessity control:

The same trained Reader is evaluated on EVAL with its selected scalar replaced by zero. EVAL is
class-balanced and the Reader receives neither query ID nor status, so any constant prediction has
exactly:

```text
zero-readout EVAL accuracy = 1/3
```

The registered gate requires this exact control within numerical tolerance.

All three saved checkpoints must round-trip exactly by weight fingerprint.

## Interpretation boundary

PASS means only:

> on this small synthetic three-value task, an isolated learned Reader can decode oracle-selected
> FOLD-R memory output and generalize across withheld alpha/beta pair compositions, with identical
> predictions before and after H1->H2 commit.

PASS does not establish:
- learned Port Selector;
- learned Writer;
- learned Coverage classifier;
- unseen semantic-value extrapolation;
- natural-language memory;
- memory-cost advantage;
- Gate F.

The next component remains unregistered until C216 is formally judged.
