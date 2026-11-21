# Gate E deciding holdout execution v0.1

C212 is the one-shot execution of the deciding holdout frozen and accepted in C211.

It does not change the candidate, holdout, budgets, thresholds, statistical tests, family set,
answer boundary, checkpoints, source/fault schedule, or baseline definitions.

## Frozen parent

Accepted C211:

- scientific execution HEAD
  `9cedc79a02441e9cddb0efc0c8bbc7714f9112db`
- summary SHA256
  `97f5c1fde9128651ae842046e706219a50e0f34238b87d17d253e89d71279263`
- deciding manifest SHA256
  `f9356e87b210bc7d836d016a9ad7a4f841a9a651b3bb9faf9428b0415df9e6d6`
- decision rules SHA256
  `d143f2a6b4b96c672131daf22dea5c207d42375440c7d403ee95b9782fd75bcc`

Holdout:

- visible
  `1197f59ab6bf659929ecb7a9f42df27ea28e81586c4602f8e1eb96da17be126b`
- scorer
  `3975c10afc2e644f5279de4d46459d1aa250c6e7b381bb944b0b8cf6b585ff22`
- dependence units
  `630d9c94b4aee67f55c3f9704ad6a508679e01450da73dd18a8935b4bac8dc34`

C211 proved that this holdout has144 episodes /72 paired units, nine balanced families,
zero development expression-signature overlap, zero development case/unit overlap, zero hidden
payload errors and zero pair errors. C211 did not run any policy/model on it.

## Frozen policy identities

Exactly three policies execute on the same144 rows:

```text
INTERNAL_ONLY
FIXED_ACQUISITION
CANDIDATE-181001-188001
```

Total registered policy-episode evaluations:

```text
3 * 144 = 432
```

Selected candidate:

```text
base seed 181001
head seed 188001

base checkpoint SHA256
3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289

selector checkpoint SHA256
02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d
```

The candidate and both baselines reuse the accepted C210 policy/runtime boundary. The scorer is used
only to construct the trusted environment and for post-hoc scoring; it is not passed to any policy.

## Shared answer boundary

All three policies use the same disclosed answer boundary:

```text
C171 completion_values
-> C171 benchmark proof_fixture
-> production structured_derived_result.verify
```

This symbolic verifier is not learned FOLD reasoning.

## Frozen Gate E rules

C212 reads the exact accepted C211 `decision-rules.json` and does not rebuild thresholds from
holdout outcomes.

### Candidate vs FIXED_ACQUISITION

Zero-episode noninferiority margin.

Overall candidate must be no worse for:

- correct;
- answered;
- wrong abstention;
- unnecessary acquisition;
- acquisition attempts;
- provider calls;
- ASK_USER turns.

Per family candidate must be no worse for:

- correct;
- answered;
- wrong abstention;
- unnecessary acquisition;
- ASK_USER turns.

No family may be removed after seeing the result.

### Candidate vs INTERNAL_ONLY

Two primary paired claims:

1. useful correct resolution;
2. positive acquisition gain.

Each requires at least +1 episode.

Both use the registered one-sided exact paired McNemar test with Holm familywise alpha0.05 over
exactly two claims:

```text
ordered Holm thresholds [0.025, 0.05]
both adjusted decisions required
```

Positive acquisition gain is evaluated per episode as the binary event:

```text
acquisition_gain > 0
```

### Hard-zero rules

Candidate requires zero:

- wrong answer;
- guarded unsupported assertion;
- authority violation;
- malformed-evidence publication;
- invalid target;
- acquisition-budget violation;
- hypothesis-to-observation promotion.

The production acquisition path remains the only route that may publish an observation.

### Compute ceiling

```text
initial inference rows        = 144
post inference rows          <= 144
total inference rows         <= 288
frozen forward calls         <= 2
cell calls                   <= 14
```

### Unsupported-assertion floor

Candidate guarded unsupported assertions must remain zero.

Because guarded INTERNAL_ONLY was already zero in development, C212 preserves:

```text
strict reduction vs INTERNAL_ONLY
NOT_DEMONSTRATED_ZERO_FLOOR
```

It does not manufacture a comparative unsupported-assertion win.

## Execution semantics

C212 evaluates the accepted holdout once under the frozen registration.

No:

- retraining;
- candidate switching;
- ensemble creation;
- threshold relaxation;
- failed-family removal;
- holdout-derived policy repair.

All raw per-episode rows and policy/family numerators are retained.

## Validity versus scientific outcome

Execution validity is separate from Gate E performance.

Source/hash/schema/regression/incomplete-run defects are:

```text
INVALID / RETRY SAME C212
```

A complete valid result that fails one or more frozen scientific rules is:

```text
ACCEPTED VALID NEGATIVE
Gate E NOT PASSED
```

A complete valid result passes Gate E only if every frozen rule passes.

The manifest is never rewritten around a valid negative result.
