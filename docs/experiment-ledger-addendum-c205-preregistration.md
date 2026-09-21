# C205 preregistration — phase-0 batch-composition attribution

**C204 ACCEPTED VALID NEGATIVE. C205 ACTIVE / NOT YET JUDGED. C206 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

## Scientific question

Are the C204 gate-breaking logit maxima fully attributable to **phase0 duplicate-expanded batch
composition**, rather than structured-v2 prefix/state semantics?

The fixed C204 tolerance remains **1e-6**. No threshold is changed.

## Parent C204 valid negative

Accepted-valid-negative C204:

- execution HEAD:
  `0ef49a4f97b516a00066df4986c062f98fda676d`
- summary SHA256:
  `9c02e4dbd497fbc91ae25c02f4cc5a3baad0af8cf9cc296f2bac0f6f8ffe72e9`

C204 valid observations:
- decisions214948;
- acquisitions129124;
- final SUFFICIENT85824;
- v2 packets214948;
- learned rows214948;
- necessity prediction errors0;
- target prediction errors0;
- v2 prefix errors0;
- runtime/scientific/projection failures0;
- max necessity logit delta `5.0067901611328125e-06`;
- max target logit delta `5.7220458984375e-06`;
- scientific status FAIL because both maxima exceed1e-6.

C205 does not reinterpret or relax that C204 result.

## Attribution hypothesis

C199 phase0 writer semantics:

```text
1768 unique observable PILOT states
-> frozen necessity/target inference
-> outputs expanded to9536 coherent worlds using local_rows
```

C204 phase0 semantics:

```text
9536 coherent-world rows
-> frozen necessity/target inference directly
```

The accepted `local_rows` mapping repeats the same observable72-feature row across multiple hidden
coherent worlds. Therefore the semantic model input can be identical while matrix batch composition
differs.

## Fixed changed variable

Only phase0 cohort presentation changes:

### A. canonical unique

```text
1768 unique budget13 states
-> decision debit
-> current structured-v2 encode
-> exact72 canonical v1 prefix
-> frozen C181/C188 combined inference
-> expand output by accepted local_rows to9536
```

### B. expanded direct

```text
9536 accepted world-expanded states
-> decision debit
-> current structured-v2 encode
-> exact72 canonical v1 prefix
-> frozen C181/C188 combined inference directly
```

For every expanded row:

```text
canonical_unique_raw[local_rows] == expanded_direct_raw
```

must be exact.

## Held constant

Both paths use:
- same accepted C181 INTERNAL_SEMANTICS checkpoints;
- same accepted C188 selector checkpoints;
- same structured-v2 channel layout;
- same exact72 learned prefix;
- same raw argmax;
- BATCH1024;
- CPU float32;
- torch threads2;
- deterministic algorithms=True;
- same C199 phase0 prediction/logit reference;
- same `1e-6` tolerance.

No action runtime, provider or acquisition occurs in C205.

## Registered workload

Per model pair:

```text
canonical unique rows = 1768
expanded direct rows  = 9536
```

Across9 model pairs:

```text
canonical rows          15912
expanded rows           85824
canonical forward calls 18
expanded forward calls  90
canonical cell calls    126
expanded cell calls     630
```

## Fixed PASS gate

All9 canonical-unique records require:

```text
prefix errors                     0
expanded-prefix mismatches        0
necessity prediction errors       0
target prediction errors          0
max necessity logit delta         <= 1e-6
max target logit delta            <= 1e-6
```

All9 expanded-direct records require:

```text
prefix errors                     0
necessity prediction errors       0
target prediction errors          0
max necessity logit delta         > 1e-6
max target logit delta            > 1e-6
```

For every block:

```text
expanded phase0 necessity max == C204 whole-loop block necessity max   within 1e-12
expanded phase0 target max    == C204 whole-loop block target max      within 1e-12
```

Workload must equal the exact registered totals above.

A valid complete miss is **ACCEPTED VALID NEGATIVE**.

Source/hash/schema/checkpoint/model/reference/regression/incomplete/protection failure is
**INVALID EXECUTION / RETRY SAME C205**.

## Interpretation boundary

PASS supports:

> the **gate-breaking maxima** observed in C204 are already completely reproduced by phase0
> duplicate-expanded batching, while the canonical unique structured-v2 path remains inside the
> original1e-6 tolerance.

PASS does **not**:
- retroactively change C204 from ACCEPTED VALID NEGATIVE to PASS;
- prove every nonzero later-phase floating-point difference is batch-derived;
- establish independent generalization;
- establish learned channel preference;
- complete Gate E.

FAIL means the C204 gate-breaking maxima cannot be fully attributed to this single batching
difference under the registered test.

## Scope

C205 registers:
- training0;
- fresh seeds0;
- acquisitions0;
- network calls0;
- production runtime modifiedFalse;
- Gate E candidateFalse.

## Authoring quality gate

C205 OWN:
- `fold_lm/v05_benchmarks/gate_e_c205_phase0_batch_composition_attribution.py`
- `tests_lm/test_v05_c205_phase0_batch_composition_attribution.py`
- `tools/run_c205.ps1`
- `tools/invoke_c205.ps1`
- this preregistration;
- `docs/phase0-batch-composition-attribution-v0.1.md`

Historical dynamic regression exclusion:

```text
tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state
```

This exact accepted C204 test reads the mutable current handoff and asserts C204 ACTIVE. It is
excluded only by exact ID because C205 correctly makes C205 active. Accepted C204 source/test bytes
remain untouched. C205 adds an immutable replacement test that verifies the exclusion identity,
single-occurrence requirement and final1871 suite size.

Expected:
- source pins44;
- protected inputs92;
- output artifacts5;
- new tests26;
- focused regression **1871 =1846 inherited -1 exact mutable historical test +26 C205 tests**;
- regression modules **90**.

Scientific manifest SHA256:

`316f8ec5e4654a321aff67ddf48e067feb29cf786e330697230ad3187e6f8c0c`

## Post-authoring review requirement

Before execution, committed remote bytes must be independently reviewed for:
- C204 accepted-valid-negative summary semantics;
- C199 phase0 unique-cache writer semantics and local_rows expansion;
- C181/C188 checkpoint identities;
- exact canonical/expanded input-prefix equality check;
- C204 block-max comparison logic;
- unchanged1e-6 tolerance;
- all source-string assertions against exact target functions;
- PowerShell launcher syntax structure and active C205 formal-state resolution;
- C205 launcher parses `run_c205.ps1` with `Parser.ParseFile` before logging/execution;
- source/protected/module/test/artifact counts;
- C206 non-registration.

Until review passes:

`post_authoring_review = PASS`

recovery review HEAD:
`2bd2ec0424db21e8ed2bfa0c7be07f8148d69afa`

Committed remote review verified that the accepted C204 test blob is unchanged, the historical
mutable-state exclusion is one canonical exact test ID with an exact-once guard and no wildcard
matching, the loaded suite is1872 candidates ->1871 executed tests, C205 contributes26 immutable
tests including the replacement contract, the runner uses `regression_suite()`, source/protected
counts remain44/92, and the dispatcher -> C205 launcher -> C205 runner parser guards remain before
scientific execution/logging.

## Execution / stop

User-facing execution uses `tools/invoke_active.ps1`.

Expected progress:
- active_experiment = C205
- C205 repository preflight
- Python syntax preflight
- source/artifact precheck PASS
- focused regression1871/1871
-9 attribution progress records
- RESULT
- POSTCHECK
- remote log publication

Judge C205 before any C206 registration.
