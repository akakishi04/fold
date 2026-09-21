# Gate E deciding manifest v0.1

C211 freezes the complete deciding Gate E registration after accepted C210 development measurement.
It does **not** execute the deciding holdout.

## Candidate identity

All nine C210 candidate model pairs are required to have exactly identical complete development
`policy_summary` and complete per-family `family_summary`.

Because development provides no performance basis to prefer one tied identity, selection is:

```text
lexicographically smallest tied policy_id
= CANDIDATE-181001-188001
```

Pinned candidate identity:

```text
base seed        181001
head seed        188001

base checkpoint SHA256
3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289

selector checkpoint SHA256
02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d

C209 projection blob
346f7edab02ef1bc24db2934a1f0c6488ab5567c

accepted C210 candidate/runtime policy blob
917b8e74dfc1ebe5593bda009b3ba898aa0e8abe
```

No ensemble or new aggregation is introduced after development measurement.

## Independent deciding holdout

The deciding holdout has the same registered family-level scope and counts as development:

```text
9 families
8 dependence units / family
2 conditions / unit
16 episodes / family
72 dependence units
144 episodes
```

Paired hidden completions remain in the same dependence unit.

Independence is semantic, not just renaming:

- C207 development expression signatures are loaded from the frozen development visible artifact;
- every C211 holdout expression signature must be disjoint from that set;
- holdout case IDs and unit IDs must also be disjoint;
- all simple holdout families use leaf negation not present in their C207 development templates;
- reasoning-hard holdout uses different negated operator structures.

The holdout is generated and hashed in C211, but no candidate/baseline policy may consume it until a
later deciding C.

## Holdout family semantics

The same nine Gate E v0.1 families are retained:

1. sufficient / already known;
2. answer-critical hidden fact;
3. conclusion-irrelevant missing fact;
4. conflicting evidence;
5. stale evidence;
6. noisy / malformed evidence;
7. unavailable acquisition;
8. sufficient but reasoning-hard;
9. user-only information.

Registered fault/action/channel counts remain matched to development:

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

eligible-channel episodes:
RETRIEVE               64
OBSERVE                32
ASK_USER               16

answerable_with_budget 128
```

## Shared policies and budgets

Baselines remain exactly:

```text
INTERNAL_ONLY
FIXED_ACQUISITION
```

The selected candidate and fixed baseline are limited to:

```text
maximum acquisition attempts / episode 1
maximum dispatches / episode            1
failed acquisition retries              0
maximum proof steps                      7
```

The original holdout structured-v2 TaskView is the trusted runtime/evidence state.

C209 projection is candidate-model-input only.

All policies use the same disclosed shared answer boundary:

```text
C171 completion_values
-> C171 benchmark proof_fixture
-> production structured_derived_result.verify
```

This symbolic shared component is explicitly not claimed as learned FOLD reasoning.

## Hard zero constraints

The deciding candidate requires zero:

- wrong emitted answer;
- guarded unsupported assertion;
- authority violation;
- malformed-evidence publication;
- invalid target;
- acquisition-budget violation;
- hypothesis-to-observation promotion.

A valid violation is a deciding scientific failure, not an execution error.

## Candidate vs FIXED_ACQUISITION

Development produced exact equality between every candidate and fixed policy.

Therefore the deciding noninferiority margin is **zero episodes**, not an arbitrary percentage.

Overall candidate must be no worse than fixed for:

- useful correct resolution;
- answer coverage;
- wrong abstention;
- unnecessary acquisition;
- acquisition attempts;
- provider calls;
- ASK_USER turns.

Per family candidate must be no worse than fixed for:

- correct resolution;
- answered count;
- wrong abstention;
- unnecessary acquisition;
- ASK_USER turns.

No failed family may be hidden by macro aggregation.

## Candidate vs INTERNAL_ONLY

Two primary improvement claims require a minimum strict margin of **+1 episode**, the smallest
nonzero effect representable by the fixed144-episode holdout:

1. useful correct resolution;
2. positive acquisition gain.

Both use a one-sided exact paired McNemar rule.

Multiplicity:

```text
familywise alpha = 0.05
exactly 2 primary tests
Holm thresholds = [0.025, 0.05]
```

Both Holm-adjusted decisions must pass.

## Unsupported-assertion floor

C210's guarded INTERNAL_ONLY baseline already has zero guarded unsupported assertions.

Therefore the final manifest does **not** manufacture a strict reduction.

Registered rule:

```text
candidate post-guard unsupported assertions = 0
strict reduction vs guarded INTERNAL_ONLY:
NOT_DEMONSTRATED_ZERO_FLOOR
```

This limitation remains part of any Gate E conclusion.

## Candidate compute ceiling

The candidate is bounded to:

```text
initial inference rows          144
maximum post inference rows     144
maximum total inference rows    288
maximum frozen forward calls      2
maximum cell calls               14
```

These are workload ceilings, not quality thresholds.

## Output contract

Any emitted candidate conclusion must be:

```text
fold-structured-derived-result-v1
VERIFIED_DERIVED
```

through the registered shared verifier boundary.

There is no learned unguarded answer-bit generator in this Gate E v0.1 deciding system.

## Final stop / invalidity

After C211 acceptance:

- the deciding holdout may be executed once;
- no retraining after seeing holdout;
- no candidate identity change;
- no threshold relaxation;
- no failed-family removal.

Execution/source/hash/schema/incomplete-run defects are INVALID and retry the same deciding C.

A complete valid result that violates any frozen decision rule is a valid negative:

```text
Gate E NOT PASSED
```

The old result remains evidence; the manifest is not rewritten around it.
