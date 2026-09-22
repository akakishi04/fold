# V5-F live Coverage dispatch v0.1

## Why C221 follows C220

C220 passed its registered offline composition check. Its `reader_predictions()` computes
expected-readable answers before `integration_results()` combines them with learned Coverage.
That is evidence of compatible component outputs, not of a Coverage decision preventing actual
runtime work. C221 changes only this causal dispatch boundary.

## One question

With the same frozen Writer/Coverage/Selector/Reader checkpoints and the same eight C220 episode
shapes, does Coverage-first dispatch preserve the accepted results while actually controlling
Selector, provider and Reader invocation?

No training, new semantic tasks, acquisition, RETRACT/ASSUME, joint optimization or cost comparison.

## Runtime interface

`fold_lm/v05/memory_dispatch.py` defines a request with only:

- seven-dimensional runtime Coverage features;
- four-dimensional structured query features;
- a callable provider closing over the actual bank state and target scope/factor.

It receives no expected class, expected answer, episode label, teacher result, or precomputed Reader
prediction. The benchmark/scorer retains those separately and compares only after dispatch returns.

The learned proposal determines the call path:

```text
Coverage says MISSING / OUT_OF_SCOPE:
    Coverage -> distinct suppression; return immediately

Coverage says SUPPORTED / HOT_REQUIRED:
    Coverage -> Selector -> provider -> Reader -> answer
```

`bank.read()` is inside the provider. It is not called when building the request or precomputing
Coverage inputs. Construction/commit numeric checks inherited from C220 are not query bank reads.

## Separate runtime safety boundary

The provider independently checks the actual target scope and presence of an observed factor.
A missing factor or ended scope is not converted into the numeric zero of an empty capsule.
A blocked or numerically unsafe provider result never exposes a Reader input.

These are deterministic preconditions, not a claim that the learned classifier guarantees safety.
A false readable Coverage prediction still counts as a classification error in the main experiment,
even when the provider prevents an invalid read.

## Main comparison

Keep the C220 episode plan unchanged:

```text
MISSING alpha; OUT_OF_SCOPE beta;
HOT alpha; SUPPORTED alpha; HOT beta; SUPPORTED beta;
REPLACE alpha; REPLACE beta.
```

Three frozen checkpoints per component give81 combinations and648 main decisions:
486 readable and162 suppressed. These are eight reused synthetic episode shapes, not648 independent
new problems or a fresh deciding holdout.

Load C220 `combination-results.json` through an exact adapter validating81 unique seed combinations,
eight unique episode labels per combination, successful parent decisions and expected/predicted
Coverage/answer fields. This artifact is scorer-only. Require648/648 live-result parity.

Expected successful main invocation totals:

| Operation | Count |
|---|---:|
| Coverage forward | 648 |
| Selector forward | 486 |
| Provider invocation | 486 |
| Numeric bank read | 486 |
| Reader forward | 486 |
| Downstream calls on the162 suppressed decisions | 0 |

Required traces are exactly `coverage` for suppression and
`coverage, selector, provider, reader` for answers.

## Causal controls

For each of81 checkpoint combinations, run four separately scored interventions. The wrapper calls
the original frozen Coverage model, records its original class, then replaces only its returned
proposal. Checkpoints, requests and actual states remain unchanged.

| Actual case | Forced Coverage proposal | Required effect |
|---|---|---|
| HOT alpha | MISSING | SUPPRESS_MISSING; no downstream calls |
| SUPPORTED beta | OUT_OF_SCOPE | SUPPRESS_OUT_OF_SCOPE; no downstream calls |
| MISSING alpha | SUPPORTED | Selector/provider called; provider blocks MISSING; no bank read or Reader |
| OUT_OF_SCOPE beta | HOT_REQUIRED | Selector/provider called; provider blocks OUT_OF_SCOPE; no bank read or Reader |

The324 controls require324 Coverage forwards,162 Selector/provider invocations and zero numeric
bank reads/Reader forwards. They test intervention effects, not task-answer accuracy; forced wrong
proposals are intentionally not treated as normal model predictions.

## Workload and scoring

Frozen Writer targets are evaluated in three batches, exactly as in C220. Main queries and controls
are dispatched individually, without reusing precomputed Reader answers across Coverage seeds.

At a successful result: Writer3 + Coverage972 + Selector648 + Reader486 =2109 model forwards.
The higher count than C220 is deliberate evidence of actual invocation, not a regression in a
claimed speed benchmark. This experiment makes no speed or total-memory-cost claim.

Keep C220 operation construction:18 learned Writer applications,12 oracle initialization writes,
3 oracle END_SCOPE operations and18 commits. Operation kind and structured query construction
remain oracle. No checkpoints are trained or updated.

A complete run with wrong predictions, differing parent answers, changed invocation traces or failed
intervention effects is a scientific FAIL. Artifact/source/schema errors, malformed model outputs
or incomplete execution are INVALID. Model-dependent downstream counts are scientific metrics;
they are not required to take their successful values before a valid negative can be serialized.

## PASS and limits

Require648 main successes/parities,486 readable successes,162 correct suppressions,324 successful
controls, exact invocation totals/order, no suppressed downstream work, unchanged fingerprints,
Writer accuracy1.0 and training0.

PASS supports causal execution of this frozen structured memory stack only. It does not pass Gate F.
Retraction/hypothesis lifecycle integration, broader unseen tasks, native operation selection,
acquisition, bounded indexing and total memory-cost comparisons remain separate work.
