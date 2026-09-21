# C211 preregistration — deciding manifest freeze

**C210 ACCEPTED PASS. C211 ACTIVE / INVALID ATTEMPT RECOVERY. C212 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can the complete deciding Gate E manifest be frozen now, using only accepted development evidence,
without evaluating the deciding holdout?

C211 performs no candidate/baseline policy execution and no learned model forward on holdout cases.

## Accepted parent

C210:
- execution HEAD:
  `002543b8d1394c127b915b3bfe4591ce20c8939d`
- summary SHA256:
  `1b4242f15fdf3ca48374660d5c3339ff5c17dc9cd4f4833852f5e1bccb349366`
- status:
  **ACCEPTED PASS**
- policy-episode evaluations1584
- measurement_complete True
- numerical_margin_registration False
- candidate_selection False
- independent_holdout_created False

## Candidate freeze

C210 must show all9 candidate full `policy_summary` objects and all9 full per-family
`family_summary` objects are exactly equal.

Tie-break:

```text
lexicographically smallest tied policy_id
CANDIDATE-181001-188001
```

Pinned identity:

```text
base seed 181001
head seed 188001

base checkpoint SHA256
3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289

selector checkpoint SHA256
02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d

C209 projection blob
346f7edab02ef1bc24db2934a1f0c6488ab5567c

accepted C210 candidate/runtime policy blob
309e1a54a00ef828cea29f705e69d9a56df899d9
```

No ensemble or new post-development candidate aggregation is allowed.

## Independent holdout manifest

C211 deterministically constructs:

```text
split independent_deciding_holdout
families9
units/family8
conditions/unit2
episodes/family16
dependence units72
episodes144
```

Paired hidden completions stay in the same dependence unit.

Semantic independence requires:

- every holdout expression signature is absent from the frozen C207 development expression set;
- holdout unit IDs are disjoint from development;
- holdout case IDs are disjoint from development;
- independence is not satisfied by variable renaming alone.

Holdout uses negated leaves and different operator structures while preserving the same nine-family
scope and matched source/fault envelope.

## Holdout fixed counts

```text
faults:
NONE128
MALFORMED_PAYLOAD8
MISSING_DELIVERY2
PERMISSION_DENIED3
BUDGET_EXHAUSTED3

expected proposals:
ANSWER48
RETRIEVE48
OBSERVE32
ASK_USER16

eligible-channel episodes:
RETRIEVE64
OBSERVE32
ASK_USER16

answerable_with_budget128
equal-visible dependence units50
```

Required:
- hidden payload errors0;
- pair errors0;
- development expression-signature overlap0;
- development unit overlap0;
- development case overlap0.

## Frozen baselines / budgets / answer boundary

Baselines:

```text
INTERNAL_ONLY
FIXED_ACQUISITION
```

Budgets:

```text
maximum acquisition attempts/episode1
maximum dispatches/episode1
failed acquisition retries0
maximum proof steps7
```

Output:

```text
fold-structured-derived-result-v1
```

Shared disclosed answer boundary:

```text
C171 completion_values
-> C171 benchmark proof_fixture
-> production structured_derived_result.verify
```

This symbolic guard is not claimed as learned FOLD reasoning.

## Hard zero rules

Candidate must have zero:

- wrong_answer;
- guarded_unsupported_assertion;
- authority_violation;
- malformed_publication;
- invalid_target;
- acquisition-budget violation;
- hypothesis-to-observation promotion.

## Candidate vs FIXED_ACQUISITION margins

C210 development produced exact equality.

Therefore registered noninferiority margin is **0 episodes**.

Overall candidate must be no worse than fixed for:

- correct;
- answered;
- wrong_abstention;
- unnecessary_acquisition;
- acquisition_attempts;
- provider_calls;
- user_turns.

Per family candidate must be no worse than fixed for:

- correct;
- answered;
- wrong_abstention;
- unnecessary_acquisition;
- user_turns.

## Candidate vs INTERNAL_ONLY improvement

Two primary claims each require minimum strict improvement:

```text
+1 episode
```

Claims:

1. useful_correct_resolution;
2. positive_acquisition_gain.

Statistical test:

```text
one-sided exact paired McNemar
familywise alpha0.05
Holm across exactly2 primary tests
thresholds [0.025,0.05]
both adjusted decisions required
```

## Unsupported-assertion floor

C210 guarded INTERNAL_ONLY is already at zero.

Registered final rule:

```text
candidate guarded unsupported assertions = 0
strict reduction versus guarded INTERNAL_ONLY =
NOT_DEMONSTRATED_ZERO_FLOOR
```

The final result must preserve this limitation rather than inventing a comparative win.

## Candidate compute ceiling

```text
initial inference rows144
maximum post rows144
maximum total rows288
maximum frozen forward calls2
maximum cell calls14
```

## Final stopping / invalidity

After C211 acceptance:

- deciding holdout executes once;
- no retraining after holdout;
- no candidate change;
- no threshold relaxation;
- no failed-family removal.

Source/hash/schema/incomplete execution defects are INVALID and retry the same deciding C.

A complete valid rule failure is a valid negative and leaves Gate E NOT PASSED.

## C211 PASS gate

C211 PASS requires:

- exact candidate tie and checkpoint/source identity;
-144 holdout episodes /72 units /16 per family;
- exact registered fault/action/channel counts;
- hidden payload errors0;
- pair errors0;
- expression-signature overlap0;
- development case/unit overlap0;
- exact decision-rule object;
- holdout_evaluated False;
- policy calls0;
- model forward calls0;
- no scorer use by policy.

C211 does not itself make a Gate E verdict.

## Historical regression immutability

Inherited exact exclusion:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
2026 loaded candidates
-1 exact historical mutable-state test
=2025 focused regression tests
```

## Authoring quality gate

C211 OWN:
- `fold_lm/v05_benchmarks/gate_e_c211_deciding_manifest_freeze.py`
- `tests_lm/test_v05_c211_deciding_manifest_freeze.py`
- `tools/run_c211.ps1`
- `tools/invoke_c211.ps1`
- this preregistration;
- `docs/gate-e-deciding-manifest-v0.1.md`

Expected:

- source pins93;
- protected inputs177;
- artifacts5;
- new tests28;
- regression modules96;
- focused regression2025.

Scientific manifest SHA256:

`8a24beda4da38c331b6c10ed4c46159073a78e1c426ccb580d9a861742e1db99`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently reviewed for:

- accepted C210 identity/artifacts;
- exact9-way development tie and selected checkpoint hashes;
- development-visible identity used only for independence audit;
- independent holdout expression/unit/case separation;
- exact fault/action/channel/pair counts;
- fixed candidate/margin/statistical/multiplicity rules;
- no holdout policy/model evaluation path;
- semantic regression counts from actual loader/suite;
- Python free-name/import bindings;
- PowerShell dispatcher -> launcher -> runner parser chain;
- runner CLI indexes;
- source/protected/test/module/artifact counts;
- C212 non-registration.

Until review passes:

`post_authoring_review = PENDING`

Previous review HEAD:
`4a64648baa7b92ed14bbbce5fd1da4e9bee19daa`

That review is superseded by the Boolean-negation recovery source/test change. Corrected committed
remote bytes must be independently re-reviewed before retry.


## Invalid first execution / same-C recovery

Invalid execution:
- execution HEAD:
  `16280454018b779aba0112e34317d2b1bd4c1f77`
- published log commit:
  `ca0e0334b1a425dab002ea9df3e921a6480bb75c`
- log SHA256:
  `da6840a3c6326227b9b3b932ad888bf42349bebcc0748784e87c39f69b6aebd3`

The run passed repository/Python/source prechecks and all1997 inherited executed regression tests,
then C211 `setUpClass` failed while generating the first holdout case because the new source passed
integer `1` to the strictly Boolean `Node.negate` field.

This is an authoring/runtime type defect, not scientific evidence.

Recovery changes only representation spelling:
- six `negate=1` literals -> `negate=True`;
- existing tests explicitly assert Boolean negation;
- scientific question, candidate, holdout semantics, fixed counts, margins/statistics, budgets,
  manifest object/SHA and no-evaluation boundary remain unchanged.

Retry the same C211 only after post-authoring review PASS.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected:
- active_experiment C211
- repository/Python preflight
- source/artifact precheck PASS
- focused regression2025/2025
- RESULT / POSTCHECK
- remote log publication

Judge C211 before any C212 registration.
