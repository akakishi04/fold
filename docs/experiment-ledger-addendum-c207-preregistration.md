# C207 preregistration — nine-family development manifest

**C206 ACCEPTED PASS. C207 ACTIVE / NOT YET JUDGED. C208 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can all nine Gate E v0.1 families be represented in a fixed balanced **development** manifest using
only the existing structured-v1/v2 schemas and runtime metadata, with paired dependence units and
all hidden completions / semantic conclusions / necessity labels / expected actions / fault outcomes
kept strictly scorer-only?

C207 measures fixture validity only. It does not run the candidate or required baselines.

## Accepted parent

C206:
- execution HEAD:
  `814dd2b51a1ff03011aeb609eae1cd75041f1428`
- summary SHA256:
  `1fd274cc8d8686b7779838df2f62670da52ddeb87f01a026b4d96cbf62db7553`
- status:
  **ACCEPTED PASS**

C206 established the terminal derived-result output boundary. C207 changes no candidate/runtime
behavior.

## Fixed split / workload

Split:

```text
development
```

No independent holdout is created.

Nine registered families:

1. sufficient_known
2. answer_critical_hidden
3. conclusion_irrelevant_missing
4. conflicting_evidence
5. stale_evidence
6. noisy_malformed_evidence
7. unavailable_acquisition
8. sufficient_reasoning_hard
9. user_only_information

Per family:

```text
dependence units       8
conditions per unit    2
episodes              16
```

Global:

```text
dependence units      72
episodes             144
structured-v2 roundtrips 144
```

Each dependence unit is the split/dependence unit for later baseline-development analysis.

## Visible packet contract

`development-visible.json` contains only:

- case_id
- unit_id
- family
- condition
- canonical structured-v2 packet

The packet may contain only fields already registered in structured-v1/v2:
- expression/tree;
- fact IDs/status;
- actually OBSERVED values and references;
- evidence time/revision;
- runtime budget/availability/permission/outcome;
- semantic per-fact channel eligibility.

Any non-OBSERVED fact must carry no value payload.

## Scorer-only contract

`development-scorer.json` contains evaluator-only:

- source_value;
- semantic_conclusion;
- answerable_with_budget;
- necessary_fact_indices;
- unnecessary_fact_indices;
- expected_proposal;
- expected_terminal;
- fault.

None of these field names or values may be serialized into the visible record outside legitimate
visible schema fields.

No scorer information is passed to a candidate in C207 because no candidate is executed.

## Pair contracts

The following families require identical visible packets across the two conditions:

- answer_critical_hidden
- conclusion_irrelevant_missing
- conflicting_evidence
- stale_evidence
- noisy_malformed_evidence
- user_only_information

Additional semantics:
- answer-critical hidden: source values0/1 produce different conclusions;
- conclusion-irrelevant missing: source values0/1 produce the same conclusion;
- conflict/stale: OBSERVE only;
- noisy/malformed: condition0 NONE, condition1 MALFORMED_PAYLOAD with the same visible packet;
- user-only: ASK_USER only.

Unavailable acquisition has a matched available control:
- permission denial: permission mask differs visibly;
- budget exhausted: acquisition budget differs visibly;
- missing delivery: visible packet remains identical to control; only scorer fault differs.

Sufficient-known and sufficient-reasoning-hard paired conditions intentionally differ in visible
observed values.

## Fixed family semantics / counts

Fault counts:

```text
NONE                 128
MALFORMED_PAYLOAD      8
MISSING_DELIVERY        2
PERMISSION_DENIED       3
BUDGET_EXHAUSTED        3
```

Expected proposal counts:

```text
ANSWER                 48
RETRIEVE               48
OBSERVE                32
ASK_USER               16
```

Episodes exposing an eligible channel:

```text
RETRIEVE               64
OBSERVE                32
ASK_USER               16
```

Answerable with the registered visible state + permitted episode envelope:

```text
128 / 144
```

## Fixed PASS gate

Required:

- episodes144;
- dependence units72;
- structured-v2 roundtrips144;
-16 episodes in each of9 families;
- exact fault/action/channel counts above;
- answerable_with_budget128;
- duplicate case IDs0;
- family count errors0;
- unit errors0;
- visible schema errors0;
- scorer leakage errors0;
- pair errors0;
- scorer contract errors0;
- hidden payload errors0;
- independent_holdout_created False.

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/parent-artifact/regression/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C207**.

No family/count/pair/fault rule may be changed after seeing C207 results.

## Scope / non-claims

C207 registers:
- candidate measurementFalse;
- baseline measurementFalse;
- numerical margin registrationFalse;
- training0;
- fresh seeds0;
- network calls0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS means only that a frozen balanced development-data boundary for all nine families exists.

PASS does not establish:
- candidate quality;
- baseline quality;
- acquisition benefit;
- unsupported assertion reduction;
- numerical acceptance margins;
- independent holdout generalization;
- final Gate E readiness or completion.

## Historical regression immutability

Inherited exact historical exclusion remains:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
1930 loaded candidates
-1 exact historical mutable-state test
=1929 executed focused regression tests
```

## Authoring quality gate

C207 OWN:
- `fold_lm/v05_benchmarks/gate_e_c207_nine_family_development_manifest.py`
- `tests_lm/test_v05_c207_nine_family_development_manifest.py`
- `tools/run_c207.ps1`
- `tools/invoke_c207.ps1`
- this preregistration;
- `docs/nine-family-development-manifest-v0.1.md`

Expected:
- source pins62;
- protected inputs122;
- output artifacts5;
- new tests28;
- focused regression **1929**;
- regression modules **92**.

Scientific manifest SHA256:

`d9d3ea599b19f1c7fa91af9e1d0a96287391ae8d4ea88b91449cb5ad4ff61f72`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently re-fetched and reviewed for:

- accepted C206 parent identity;
- all9 family names and exact balanced counts;
- dependence-unit binding identity;
- visible/scorer structural separation;
- non-OBSERVED no-payload rule;
- hidden-pair packet equality / conclusion-difference rules;
- fault/action/channel exact counts;
- no candidate/baseline/holdout claim;
- semantic regression counts from actual loader/suite;
- Python free-name/import binding in benchmark/tests;
- PowerShell dispatcher -> launcher -> runner parser chain;
- source/protected/test/module/artifact counts;
- C208 non-registration.

Until review passes:

`post_authoring_review = PASS`

review HEAD:
`5d2115e39f3986513387281ec8de3f1723cbcfc1`

Committed remote review verified accepted C206 execution/source identity, all9 family names, balanced
144-episode /72-unit fixture counts, dependence-unit binding identity, visible/scorer separation,
non-OBSERVED no-payload checks, hidden-pair equality/difference contracts, exact fault/action/channel
counts, no candidate/baseline/holdout claim, 28 C207 tests, semantic1930-loaded/1929-kept regression
accounting, zero unbound executable c### aliases in benchmark/tests, runner/launcher argument wiring,
PowerShell parser chain, 62 source pins /122 protected inputs /5 artifacts, and C208 non-registration.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected progress:
- active_experiment = C207
- C207 repository preflight
- Python syntax preflight
- source/artifact precheck PASS
- focused regression1929/1929
- RESULT
- POSTCHECK
- remote log publication

Judge C207 before any C208 registration.
