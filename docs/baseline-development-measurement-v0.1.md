# Gate E baseline-development measurement v0.1

C210 performs the separate baseline-development measurement required before numerical Gate E
margins are frozen.

It is **not** a performance acceptance gate and does not evaluate an independent holdout.

## Frozen development data

C207 development manifest:

- 144 episodes
- 72 dependence units
- 9 registered families
- visible SHA256
  `c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543`
- scorer SHA256
  `0591682848a69ac020a0f4a7bb2939e6df79ffd116567fe3c994a5f8e3fa3912`

C209 projection is used only for frozen learned candidate input. The original structured-v2
TaskView remains the trusted runtime/evidence state.

## Policy identities

Measure11 policies on the same144 episodes:

```text
INTERNAL_ONLY
FIXED_ACQUISITION

CANDIDATE-181001-188001
CANDIDATE-181001-188002
CANDIDATE-181001-188003
CANDIDATE-181002-188001
CANDIDATE-181002-188002
CANDIDATE-181002-188003
CANDIDATE-181003-188001
CANDIDATE-181003-188002
CANDIDATE-181003-188003
```

Total policy-episode evaluations:

```text
11 * 144 = 1584
```

No candidate identity is selected in C210.

## Shared answer boundary

Every policy uses the same disclosed bounded answer component:

```text
C171 completion_values
-> C171 benchmark-only proof_fixture
-> production structured_derived_result.verify
```

This is a symbolic shared answer boundary, not learned FOLD reasoning.

It emits an answer only when the current trusted visible evidence logically determines one Boolean
conclusion and the production verifier accepts the supporting proof.

Therefore C210 can measure guarded useful resolution/coverage and acquisition policy behavior. It
does not claim to measure an unguarded learned answer-bit hallucination rate because such a learned
answer generator is not present.

## INTERNAL_ONLY

- no acquisition;
- no provider access;
- resolve only from initial trusted visible state.

The registered development fixture implies:

```text
correct/answered 48
unresolved       96
attempts          0
provider calls    0
publications      0
user turns        0
```

These structural baseline counts are a harness control, not a Gate margin.

## FIXED_ACQUISITION

1. run the shared resolver;
2. if unresolved, select the first non-OBSERVED original fact in canonical `fact_id` order that
   declares exactly one acquisition channel;
3. make at most one real acquisition attempt through the production runtime;
4. run the shared resolver again.

The fixed baseline never receives necessity labels or hidden values.

Registered development-harness control totals:

```text
correct/answered 128
unresolved        16
attempts           96
provider calls     90
publications       80
ASK_USER turns     16
authority violations0
```

The16 unresolved cases are the registered malformed/unavailable development fault cases.

## Frozen candidate cohort

For each of the9 accepted C181/C188 model pairs:

1. project the initial visible TaskView through C209;
2. run frozen combined necessity/target inference;
3. if necessity says SUFFICIENT, invoke the shared resolver on the trusted original runtime state;
4. if necessity says NEEDS and the selected target maps to an original projected-UNOBSERVED fact,
   route the selected fact through the original structured-v2 channel metadata and production
   acquisition runtime;
5. after one successful publication, project the updated trusted state and run one frozen necessity
   reclassification;
6. emit only if that learned post state says SUFFICIENT and the shared resolver verifies;
7. never retry a failed acquisition and never acquire more than once in this development measurement.

No scorer field reaches this policy function.

## Development environment faults

Scorer metadata configures only the trusted environment and post-hoc scoring.

Registered source behaviors:

- NONE: valid bounded source delivery;
- MALFORMED_PAYLOAD: one provider call, rejected by production source validation;
- MISSING_DELIVERY: one provider call returning no delivery;
- PERMISSION_DENIED: runtime denies before provider call;
- BUDGET_EXHAUSTED: runtime denies before provider call.

The same production acquisition lifecycle is used by candidate and fixed baseline.

## Raw metrics

Per policy and family record raw numerators/denominators for:

- answered / unresolved;
- useful correct resolution;
- wrong answer;
- wrong abstention;
- pre-resolved / pre-correct;
- acquisition gain;
- acquisition attempts;
- provider calls / publications;
- ASK_USER turns;
- unnecessary acquisition;
- missed necessary acquisition;
- authority violations;
- malformed-evidence publication;
- guarded unsupported assertion;
- internal charges;
- resolver verifier calls / checked steps;
- candidate premature-sufficient;
- candidate repeated NEEDS after successful publication;
- invalid target;
- frozen-model inference rows/calls.

No performance threshold is registered in C210.

## Interpretation boundary

C210 PASS means only that the matched development measurement is complete under the registered
policy/runtime/answer boundaries.

Candidate performance may be good or bad and still yield C210 PASS.

After C210 is accepted, a later preregistered step may use **only these development results** to:
- freeze one candidate identity or a predeclared candidate aggregation;
- freeze numerical improvement/noninferiority/coverage/cost margins;
- freeze the final holdout manifest and statistical rules.

The independent deciding holdout must not be evaluated before those choices are frozen.
