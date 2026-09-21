# C212 preregistration — deciding holdout execution

**C211 ACCEPTED PASS. C212 ACTIVE / NOT YET JUDGED. C213 NOT REGISTERED.**
Gate E remains **NOT PASSED** until C212 is judged.

## Scientific question

Under the exact accepted C211 deciding manifest, does the frozen selected candidate satisfy every
preregistered Gate E rule on the independent holdout when compared with INTERNAL_ONLY and
FIXED_ACQUISITION?

C212 is the one-shot deciding holdout execution. It performs no retraining and makes no
post-holdout change to candidate identity, thresholds, family set, budgets or statistical rules.

## Accepted parent

C211:
- execution HEAD:
  `9cedc79a02441e9cddb0efc0c8bbc7714f9112db`
- published log commit:
  `c35a76b33c1782dc6caa1916c9fc3f7658bbbba7`
- log SHA256:
  `93992504ae7dae472911521e5bed336f57407e4bc8dfc3542b6e60863da1c25c`
- summary SHA256:
  `97f5c1fde9128651ae842046e706219a50e0f34238b87d17d253e89d71279263`
- status:
  **ACCEPTED PASS**

C211 frozen artifacts:

```text
holdout-visible.json
1197f59ab6bf659929ecb7a9f42df27ea28e81586c4602f8e1eb96da17be126b

holdout-scorer.json
3975c10afc2e644f5279de4d46459d1aa250c6e7b381bb944b0b8cf6b585ff22

holdout-units.json
630d9c94b4aee67f55c3f9704ad6a508679e01450da73dd18a8935b4bac8dc34

decision-rules.json
d143f2a6b4b96c672131daf22dea5c207d42375440c7d403ee95b9782fd75bcc

deciding-manifest.json
f9356e87b210bc7d836d016a9ad7a4f841a9a651b3bb9faf9428b0415df9e6d6
```

C211 guarantees:
-144 holdout episodes;
-72 dependence units;
-9 families /16 episodes each;
- development expression-signature overlap0;
- development case overlap0;
- development unit overlap0;
- hidden payload errors0;
- pair errors0;
- holdout_evaluated False;
- model_forward_calls0;
- baseline_policy_calls0.

## Frozen candidate

Policy:

```text
CANDIDATE-181001-188001
```

Identity:

```text
base seed 181001
head seed 188001

base checkpoint SHA256
3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289

selector checkpoint SHA256
02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d
```

No alternative candidate, ensemble, checkpoint or threshold may be selected after holdout access.

## Policy workload

Exactly:

```text
INTERNAL_ONLY
FIXED_ACQUISITION
CANDIDATE-181001-188001
```

Each covers all144 holdout episodes.

Registered total:

```text
3 policies *144 episodes =432 policy-episode evaluations
```

Candidate/baseline implementation reuses the accepted C210 policy/runtime boundary.

The holdout scorer is environment-construction/post-hoc-scoring data only. It is not passed into a
policy function.

## Shared answer boundary

All policies use:

```text
C171 completion_values
-> C171 benchmark proof_fixture
-> production structured_derived_result.verify
```

This is a disclosed symbolic guard, not learned FOLD reasoning.

## Frozen C211 decision rules

C212 must load and compare against the exact accepted `decision-rules.json`. It must not
reconstruct favorable thresholds from C212 outcomes.

### Candidate vs FIXED_ACQUISITION

Noninferiority margin:

```text
0 episodes
```

Overall candidate must be no worse on:

- correct;
- answered;
- wrong_abstention;
- unnecessary_acquisition;
- acquisition_attempts;
- provider_calls;
- user_turns.

Per-family candidate must be no worse on:

- correct;
- answered;
- wrong_abstention;
- unnecessary_acquisition;
- user_turns.

A failed family cannot be hidden by aggregate success.

### Candidate vs INTERNAL_ONLY

Primary claims:

1. useful_correct_resolution;
2. positive_acquisition_gain.

Each requires:

```text
minimum strict improvement +1 episode
```

Paired test:

```text
one-sided exact McNemar
familywise alpha0.05
Holm across exactly2 primary claims
thresholds [0.025,0.05]
both adjusted decisions required
```

For the second claim, the episode-level binary event is:

```text
acquisition_gain > 0
```

## Hard-zero rules

Candidate requires zero:

- wrong_answer;
- guarded_unsupported_assertion;
- authority_violation;
- malformed_publication;
- invalid_target;
- acquisition_budget_violations;
- hypothesis_to_observation_promotions.

## Compute ceiling

```text
initial inference rows =144
post inference rows <=144
total inference rows <=288
frozen forward calls <=2
cell calls <=14
```

## Unsupported-assertion floor

Required:

```text
candidate guarded unsupported assertions =0
strict reduction vs guarded INTERNAL_ONLY =
NOT_DEMONSTRATED_ZERO_FLOOR
```

The already-zero guarded INTERNAL_ONLY baseline cannot support a strict reduction claim.

## Fixed execution behavior

C212:
- holdout execution count1;
- retraining0;
- fresh seeds0;
- network0;
- production runtime modifications0;
- candidate changes0;
- threshold changes0;
- failed-family removals0.

All raw episode rows and raw policy/family numerators are retained.

## C212 scientific PASS gate

A complete valid C212 result passes Gate E only if all are true:

- all3 policies cover all144 episodes;
-432 policy-episode records are present exactly once;
- every hard-zero rule is0;
- overall zero-margin noninferiority vs FIXED_ACQUISITION passes;
- every per-family no-worse-than-fixed rule passes;
- both +1 minimum improvement claims vs INTERNAL_ONLY pass;
- both one-sided exact McNemar tests pass the registered two-claim Holm procedure;
- candidate compute ceiling passes;
- output floor/verified-emission rule passes;
- accepted C211 artifacts/rules/checkpoints remain byte-identical.

A valid complete scientific rule failure is not INVALID. It is:

```text
ACCEPTED VALID NEGATIVE
Gate E NOT PASSED
```

## Invalidity / retry

Only execution-validity failures permit the same C212 to retry:

- wrong source/artifact hash;
- schema mismatch;
- wrong branch/HEAD;
- regression failure;
- incomplete policy/family/episode coverage;
- artifact corruption;
- nonfinite or runtime exception before a valid complete result.

Do not relax any scientific rule to convert a valid negative into PASS.

## Historical regression immutability

Inherited exact exclusion:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
2056 loaded candidates
-1 exact historical mutable-state test
=2055 focused regression tests
```

## Authoring quality gate

C212 OWN:
- `fold_lm/v05_benchmarks/gate_e_c212_deciding_holdout_execution.py`
- `tests_lm/test_v05_c212_deciding_holdout_execution.py`
- `tools/run_c212.ps1`
- `tools/invoke_c212.ps1`
- this preregistration;
- `docs/gate-e-deciding-holdout-execution-v0.1.md`.

Expected:
- source pins99;
- protected inputs189;
- output artifacts5;
- new tests30;
- regression modules97;
- focused regression **2055**.

Scientific manifest SHA256:

`1e9c1fd0de152ccd070a267383e46fbe73ff5c55114fe984c85ecd7274347898`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently re-fetched and reviewed for:

- accepted C211 summary/artifact identity;
- exact deciding-manifest/rules/holdout hashes;
- selected checkpoint identity;
- exactly3 policies /432 episode evaluations;
- scorer separation from policy functions;
- exact fixed-noninferiority metrics/operators;
- exact INTERNAL_ONLY improvement claims and paired binary definitions;
- exact McNemar/Holm multiplicity;
- hard-zero and compute rules;
- valid-negative versus INVALID separation;
- no retraining/candidate/threshold/family adaptation;
- semantic regression counts from actual loader/suite;
- Python free-name/import bindings;
- PowerShell dispatcher -> launcher -> runner parser chain;
- runner CLI argument indexes/order;
- source/protected/test/module/artifact counts;
- C213 non-registration.

Until review passes:

`post_authoring_review = PENDING`

Do not issue the C212 execution command before post-authoring review PASS.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected progress:
- active_experiment = C212;
- C212 repository preflight;
- Python syntax preflight PASS;
- source/artifact precheck PASS;
- focused regression2055/2055;
- one deciding holdout execution;
- RESULT;
- POSTCHECK;
- remote log publication.

Judge the complete C212 result before registering any C213.
