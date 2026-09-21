# C208 preregistration — candidate input compatibility preflight

**C207 ACCEPTED PASS. C208 ACTIVE / NOT YET JUDGED. C209 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Can the current frozen C181/C188 candidate inference interface consume all144 frozen C207 visible
development packets **as-is**, without representation adaptation, scorer leakage or schema
reinterpretation?

C208 performs no model forward and no baseline measurement.

## Frozen parent / input

C207:
- execution HEAD:
  `96020d20bd73bf6e2e62d5bfb202b7b2605a2079`
- summary SHA256:
  `a7e69871003ac1978e786809c822d75c0dc291cfbe14aa8709f8b12ec26e4477`
- visible artifact SHA256:
  `c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543`
- status:
  **ACCEPTED PASS**

Only the frozen C207 `development-visible.json` artifact is loaded.

The C207 scorer artifact is not loaded or used.

## Candidate input contracts

C208 pins the current source blobs:

```text
C178 visible-leaf-binding
2ec87851f1f75533dd2225243d0c1baeda9c9a2a

C188 multimissing target selector
0819bc70377a949fe1c17a66be559336bbda96e1
```

### Necessity path

Actual validator path:

```text
C207 structured-v2 packet
-> exact first72 structured-v1 features
-> C178 prepare_pair / validate_raw
```

### Target path

Actual validator path:

```text
same exact72 features
-> C188 missing_mask
-> C188 leaf_positions
```

No model forward is permitted.

## Per-case classification

For each of144 cases record:

- family / dependence-unit / condition;
- exact7-node/4-fact header compatibility;
- active fact-slot count;
- active FACT-leaf count;
- whether active fact statuses are C188-compatible;
- C178 necessity input acceptance / exact rejection reason;
- C188 target input acceptance / exact rejection reason;
- combined acceptance.

Expected validator rejection is a scientific compatibility result, not execution invalidity.

Only unexpected harness/source/schema failures invalidate the execution.

## Scientific PASS gate

C208 PASS requires:

```text
episodes               144
families                 9
classified_rows        144
unexpected_errors        0
necessity+target compatible 144
incompatible             0
model_forward_calls      0
adapter_used          False
scorer_used           False
```

Any complete valid result with one or more incompatible rows is a valid scientific miss and must be
judged **ACCEPTED VALID NEGATIVE**.

No representation adapter, family removal or schema reinterpretation may be introduced under C208.

## Execution-validity gate

Execution is valid when:

- all144 frozen visible rows are classified;
- all9 families are present with16 episodes each;
- all frozen packets roundtrip exactly;
- C207 visible artifact identity is preserved;
- C178/C188 source blobs match the preregistered identities;
- no unexpected exception escapes classification;
- model forward calls0;
- scorer useFalse;
- adapter useFalse.

Scientific incompatibility does not make execution invalid.

## Scope / non-claims

C208 registers:

- model forward calls0;
- candidate measurementFalse;
- baseline measurementFalse;
- adapter implementationFalse;
- training0;
- fresh seeds0;
- network0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

PASS only establishes as-is input compatibility.

A valid negative identifies the representation blocker that must be addressed before
baseline-development measurement.

C208 does not establish candidate quality, baseline quality, numerical Gate E margins, independent
holdout readiness or Gate E completion.

## Historical regression immutability

Inherited exact historical exclusion remains:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

Regression accounting:

```text
1950 loaded candidates
-1 exact historical mutable-state test
=1949 executed focused regression tests
```

## Authoring quality gate

C208 OWN:
- `fold_lm/v05_benchmarks/gate_e_c208_candidate_input_compatibility_preflight.py`
- `tests_lm/test_v05_c208_candidate_input_compatibility_preflight.py`
- `tools/run_c208.ps1`
- `tools/invoke_c208.ps1`
- this preregistration;
- `docs/candidate-input-compatibility-preflight-v0.1.md`

Expected:
- source pins70;
- protected inputs136;
- output artifacts5;
- new tests20;
- focused regression **1949**;
- regression modules **93**.

Scientific manifest SHA256:

`52533ba9b2057f791b55cb6d1bafebf2cedfeae0400b5ecbf0f6a661ed77e7d6`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently reviewed for:

- accepted C207 summary/visible artifact identity;
- exact C178/C188 source-blob identities;
- no scorer artifact load/use;
- no model forward or adapter path;
- classification catches expected ValueError as data and no broader exception;
- scientific PASS vs execution-validity separation;
- semantic regression counts from actual loader/suite;
- Python free-name/import bindings in benchmark/tests;
- PowerShell dispatcher -> launcher -> runner parser chain;
- runner CLI index/order;
- source/protected/test/module/artifact counts;
- C209 non-registration.

Until review passes:

`post_authoring_review = PASS`

review HEAD:
`1d115cc4e8ff9e2199388bf0108f3d11b1c72b7a`

Committed remote review verified accepted C207 summary/visible identity and all6 C207 OWN blobs,
exact C178/C188 source blobs, no scorer artifact load, no model forward or adapter path, expected
validator ValueError classification without broad exception swallowing, scientific PASS separated
from execution validity, 20 C208 tests, semantic1950-loaded/1949-kept regression accounting, zero
unbound executable c### aliases in benchmark/tests, runner CLI indexes, dispatcher->launcher->runner
PowerShell parser chain, 70 source pins /136 protected inputs /5 artifacts, and C209 non-registration.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected progress:
- active_experiment = C208
- C208 repository preflight
- Python syntax preflight
- source/artifact precheck PASS
- focused regression1949/1949
- RESULT
- POSTCHECK
- remote log publication

Judge C208 before any C209 registration.
