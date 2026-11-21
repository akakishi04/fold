# Nine-family Gate E development manifest v0.1

C207 freezes the **development-data boundary** required before baseline-development measurement.
It does not run the candidate, baselines or a deciding holdout.

## Scope

The complete Gate E v0.1 family list is represented:

1. sufficient / already known;
2. answer-critical hidden fact;
3. conclusion-irrelevant missing fact;
4. conflicting evidence;
5. stale evidence;
6. noisy / malformed evidence;
7. unavailable acquisition;
8. sufficient but reasoning-hard;
9. user-only information.

Each family has:

```text
8 dependence units
2 conditions per unit
16 episodes per family
```

Global:

```text
72 dependence units
144 development episodes
```

The split is explicitly `development`. C207 creates **no independent holdout**.

## Visible / scorer separation

Two distinct artifacts are generated.

### development-visible.json

Contains only:

- case ID;
- dependence-unit ID;
- family;
- condition index;
- canonical structured-v2 policy packet.

The packet contains only fields allowed by existing structured-v1/v2 schemas:
expression, fact statuses, observed values, evidence/reference bindings, resources and semantic
channel eligibility.

### development-scorer.json

Evaluator-only fields:

- hidden/source value;
- semantic conclusion;
- answerable-with-budget label;
- necessary/unnecessary fact indices;
- expected proposal;
- expected terminal state;
- fault schedule.

These fields never enter the visible packet.

Non-OBSERVED facts never carry a hidden value in the visible schema.

## Paired dependence units

The following families require byte-identical visible packets across the two hidden/fault
conditions:

- answer-critical hidden;
- conclusion-irrelevant missing;
- conflicting evidence;
- stale evidence;
- noisy/malformed evidence;
- user-only information.

Unavailable-acquisition units have a matched available control. Missing-delivery controls remain
visible-identical; permission-denied and budget-exhausted cases intentionally expose the relevant
runtime authority/budget difference.

Sufficient-known and reasoning-hard paired cases intentionally differ in visible observed values.

## Fixed family semantics

- answer-critical hidden: RETRIEVE is necessary;
- conclusion-irrelevant missing: ANSWER without acquisition;
- conflict/stale: OBSERVE is the only semantic channel;
- malformed: matched valid vs malformed provider outcome;
- unavailable: matched valid control vs permission denial / budget exhaustion / missing delivery;
- reasoning-hard: four observed facts and three operators, no acquisition;
- user-only: ASK_USER is the only semantic channel.

## Fixed counts

```text
faults:
NONE                 128
MALFORMED_PAYLOAD      8
MISSING_DELIVERY        2
PERMISSION_DENIED       3
BUDGET_EXHAUSTED        3

expected proposals:
ANSWER                 48
RETRIEVE               48
OBSERVE                32
ASK_USER               16

episodes exposing eligible channels:
RETRIEVE               64
OBSERVE                32
ASK_USER               16

answerable_with_budget 128
```

## Interpretation boundary

PASS means the existing bounded structured schemas can represent a balanced, paired, leakage-free
development fixture covering all nine Gate E families with exact artifact identities.

PASS does not measure:
- candidate quality;
- baseline quality;
- acquisition benefit;
- unsupported assertion rates;
- numerical acceptance margins;
- independent holdout generalization;
- final Gate E.

A later experiment must run the required baselines against this frozen development manifest before
numerical margins are chosen.
