# Mixed-channel multistep replay v0.1

C203 extends the accepted C202 one-step three-channel dispatch into a multi-step episode while
holding the learned decision trace fixed to the accepted C199 ALLOWED artifact.

## Fixed semantic channel layout

```text
fact0 -> RETRIEVE
fact1 -> OBSERVE
fact2 -> ASK_USER
fact3 -> RETRIEVE
```

The layout is visible metadata, not a learned preference.

## Parent decision state

Before every replayed learned decision, runtime masks are restored to the accepted parent state:

```text
available = [true,false,false]
permitted = [true,false,false]
```

The decision itself is not recomputed in C203; accepted C199 saved necessity/target outputs are
replayed exactly.

## Action window

After a replayed NEEDS + target decision:

1. trusted scheduler enables all three runtime channels;
2. selected fact is wrapped in the fixed structured-v2 one-hot channel metadata;
3. accepted C201 mapper creates the typed proposal;
4. existing action/acquisition runtime reserves and dispatches;
5. selected fact is published from the coherent world source;
6. trusted scheduler restores parent masks before the next decision.

Authority refreshes do not replenish or debit internal/acquisition budgets.

## Expected parent totals

The accepted parent trace fixes:

```text
episodes             85824
learned decisions    214948
acquisitions         129124
final SUFFICIENT     85824
```

Per-channel provider totals and within-episode channel-switch counts are a deterministic projection
of the accepted target indices through the fixed channel layout. They are computed from the parent
artifact before C203 execution and compared exactly with the observed dispatch trace.

## Resource contract

For an episode with D replayed decisions and A admitted acquisitions:

```text
internal_remaining      = 13 - D - 3*A
acquisitions_remaining  = 4 - A
internal_step           = 7 + D + 3*A
last_outcome            = NONE
pending                 = none
runtime terminal        = none
```

Every episode must terminate at its accepted final SUFFICIENT decision.

## Scope

C203 establishes mixed-channel multi-step orchestration for an already accepted learned decision
trace. It does not establish learned channel preference, real sensor/user transport, or final Gate E
quality.
