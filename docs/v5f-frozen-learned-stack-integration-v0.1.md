# V5-F frozen learned stack integration v0.1

C220 is the first integration test after the four V5-F learned components were accepted
individually.

## Scientific question

Can the independently accepted learned Writer, Coverage classifier, Port Selector and Reader
compose end-to-end with all checkpoints frozen and no retraining across:

- ASSERT into H1;
- HOT_REQUIRED read;
- H1 -> H2 commit;
- SUPPORTED read;
- REPLACE;
- MISSING;
- OUT_OF_SCOPE?

Operation kind remains oracle.

## No new training

C220 trains **zero** models.

Frozen accepted families:

```text
C218 Writer      3 checkpoints
C219 Coverage    3 checkpoints
C217 Selector    3 checkpoints
C216 Reader      3 checkpoints
```

Every Cartesian checkpoint combination is evaluated:

```text
3 * 3 * 3 * 3 = 81 combinations
```

## Runtime glue

New deterministic module:

`fold_lm/v05/memory_stack.py`

It does not contain learned parameters.

Coverage mapping:

```text
SUPPORTED      -> READ
HOT_REQUIRED   -> READ
MISSING        -> SUPPRESS_MISSING
OUT_OF_SCOPE   -> SUPPRESS_OUT_OF_SCOPE
```

MISSING and OUT_OF_SCOPE therefore remain distinct through the runtime gate.

## Episode plan

Eight registered episodes:

```text
1 MISSING alpha
2 OUT_OF_SCOPE beta
3 HOT alpha
4 SUPPORTED alpha
5 HOT beta
6 SUPPORTED beta
7 REPLACE alpha
8 REPLACE beta
```

Episode-plan SHA256:

`99f84e9d05327c8c483b45928676009f6be198e5d568a285d2e893e1279e144f`

Readable episodes:6.
Non-readable episodes:2.

Across81 checkpoint combinations:

```text
total decisions        648
readable decisions     486
non-readable decisions 162
```

## Writer use

The frozen Writer is evaluated on the held-out nuisance descriptor [+1,+1] for four relation
targets used by the episode plan:

```text
alpha class0
beta  class2
alpha class1
beta  class0
```

One batched Writer forward is used per Writer checkpoint.

Writer prediction is used directly as factor+relation in the MemoryOp. Operation kind remains
oracle.

## Coverage use

Coverage features are generated from the **actual state produced by the Writer path**.

For each Writer checkpoint, each of the3 frozen Coverage checkpoints classifies all8 episodes in one
batch.

Coverage is measured against:
1. the deterministic teacher for the actual produced state;
2. the preregistered expected episode status.

Thus a Writer error that changes target state cannot be hidden by a correct Coverage classifier.

## Selector / Reader use

Each frozen Selector evaluates the held-out alpha/beta query descriptors once.

For each Writer x Selector x Reader combination, all six expected-readable episode readouts are
decoded in one Reader batch.

The episode values are chosen so the intended and wrong port contain different semantic classes;
a routing error therefore cannot silently preserve the expected answer.

## Integration success

Readable episode success requires all of:

- Writer-produced state valid;
- actual target coverage equals preregistered expected coverage;
- learned Coverage prediction equals that expected coverage;
- runtime gate permits READ;
- learned Selector routes to the selected port;
- frozen Reader returns the expected semantic class.

Non-readable episode success requires all of:

- actual target coverage equals expected MISSING or OUT_OF_SCOPE;
- learned Coverage prediction equals it;
- runtime gate suppresses with the correct distinct reason.

## Placement parity

For every Writer x Selector x Reader combination:

```text
HOT alpha prediction == COMMITTED alpha prediction
HOT beta  prediction == COMMITTED beta prediction
```

Required mismatches:0.

## Fixed workload

No training.

```text
frozen Writer forwards      3
frozen Coverage forwards    9
frozen Selector forwards    3
frozen Reader forwards     27
total model forwards       42

learned Writer op slots    18
oracle initialization      12
oracle END_SCOPE ops        3
chunk-commit slots         18
```

## Fixed PASS gate

```text
all checkpoint roundtrips        true
Writer target accuracy           1.0
Selector route accuracy          1.0
Coverage teacher accuracy        1.0

checkpoint combinations          81
decision rows                   648
readable decisions              486
non-readable decisions          162

integration accuracy             1.0
expected Coverage accuracy       1.0
readable answer accuracy         1.0
non-readable suppression         1.0

MISSING/OOS confusions             0
HOT/COMMITTED mismatches           0
operation failures                 0
```

## Interpretation boundary

PASS means only that the four independently accepted learned V5-F memory components can be composed
without retraining on this small structured synthetic lifecycle.

PASS does not establish:

- learned operation-kind selection;
- RETRACT/ASSUME integration;
- information-acquisition integration;
- natural-language Writer/query inputs;
- joint training;
- memory-cost superiority versus full history;
- Gate F.

C221 remains unregistered until C220 is formally judged.
