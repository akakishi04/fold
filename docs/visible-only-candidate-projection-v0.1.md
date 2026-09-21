# Visible-only candidate projection v0.1

C209 tests a deterministic model-input projection for the representation incompatibility measured
by accepted-valid-negative C208.

## Boundary

The trusted runtime/evidence state remains the original C207 structured-v2 TaskView.

The projection exists only to feed the frozen legacy C181/C188 model interface.

It never:
- replaces the trusted runtime state;
- writes evidence;
- consumes scorer metadata;
- executes a model forward;
- changes runtime budgets/authority/channels.

## Projection rule

Original fact indices and order are preserved.

For each original fact:

- OBSERVED remains exactly OBSERVED, including its visible value/reference;
- every other registered status becomes UNOBSERVED **only in the candidate projection**;
- normalized projected facts carry no value or reference.

Until four facts exist, append architectural constants:

```text
__FOLD_CONST_TRUE_i
status    OBSERVED
value     1
```

Each appended TRUE fact is wrapped around the previous expression root:

```text
new_root = old_root AND TRUE
```

Thus:

```text
1-fact /1-node  ->4-fact /7-node
2-fact /3-node  ->4-fact /7-node
4-fact /7-node  ->unchanged shape
```

Padding facts are OBSERVED, so C188 must never mark them missing/selectable.

## Semantic controls

For every one of the144 frozen C207 episodes, exhaustively enumerate every assignment of the
**original** facts and hold each padding fact TRUE.

Projected root output must equal original root output for every completion.

Registered total truth-table checks:

```text
1-fact episodes  16 *2 assignments  = 32
2-fact episodes 112 *4 assignments  =448
4-fact episodes  16 *16 assignments =256
-----------------------------------------
total                                 736
```

## Fixed structural totals

```text
original fact counts:
1 fact   16
2 facts 112
4 facts  16

synthetic TRUE facts added   272
STALE/CONFLICT status normalizations 32
```

The50 C207 dependence units whose two source-visible packets are identical must remain identical
after projection.

## Candidate-contract controls

Every projected packet must pass, without model forward:

- C178 `prepare_pair`;
- C188 `missing_mask`;
- C188 `leaf_positions`.

All original fact indices must remain stable.

All dummy indices must map to -1 / no original fact and must be non-missing under C188.

## PASS meaning

PASS means a visible-only deterministic projection can make all144 fixed development packets legal
for the legacy frozen candidate input contract while preserving Boolean semantics and the trusted
runtime/evidence boundary.

PASS does not establish learned policy quality after projection. Baseline-development measurement
must still be performed separately.
