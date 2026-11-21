# C206 execution recovery — stale source-count assertion

## Disposition

**C206 — INVALID EXECUTION / RETRY SAME C206.**
**C207 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

Invalid execution:
- execution HEAD: `95d087011a7071ad920b9ab1620706b9e0b74205`
- published log commit: `922b51eaaf5dfbace77644d658bd4f17dab71218`
- log SHA256: `3a3d8be20e2eec475b8512a5f284bec75d5c0708b7e9f04ff5606b13506a590f`
- focused regression: **1901 tests,1900 PASS /1 FAIL**
- scientific diagnostic: **not started**
- run_execution_valid: False

## Failure

Only this C206 authoring test failed:

```text
tests_lm.test_v05_c206_terminal_derived_result_integration.C206Tests.
test_25_regression_preserves_exact_historical_exclusion
```

The implementation had already been updated to:

```text
loaded candidates =1902
kept tests        =1901
```

after adding two launcher-safety tests.

But test25 still inspected the source text and required the old literals:

```text
"len(tests) == 1900"
"len(kept) == 1899"
```

All other29 C206 tests passed.

## Root cause

This was another authoring-test maintenance bug.

The scientific regression suite implementation and runner contract were correct. The failing test
did not exercise the suite; it inspected its source string for mutable count literals.

When later authoring added two tests, the implementation count was updated but this source-string
assertion remained stale.

## Minimal recovery

Scientific conditions remain unchanged.

test25 now performs semantic validation:

1. load the actual91 regression modules;
2. flatten the actual loaded test suite;
3. require exactly1902 candidate test IDs;
4. require the one preregistered historical mutable test ID exactly once;
5. call the real `regression_suite()`;
6. require exactly1901 kept test IDs;
7. require the excluded ID absent from the kept suite.

No source-string numeric count assertion remains in test25.

## Process correction

Authoring count contracts are now required to be semantic.

Mutable counts such as:
- module count;
- loaded test count;
- exclusion count;
- post-filter suite size;

must be checked by constructing the actual loader/suite and counting cases/test IDs. They must not
be validated by searching `inspect.getsource()` for numeric literals.

C206 scientific question, workload, verifier contract, C171 lineage, mixed-channel replay and Gate
remain unchanged.

## Second invalid attempt — unbound parent-module alias

Disposition remains **INVALID EXECUTION / RETRY SAME C206**.

- execution HEAD: `ffaac098988476d2db483005d487bddd02102f32`
- published log commit: `98fb270d0dc43bf4a7c2689e985748a5c86a3196`
- log SHA256: `f9ee35e596e7e35d2340c977f0035955da188e1b404ae5a16e1d5de6dc98c77a`
- focused regression: **1901 tests,1900 PASS /1 ERROR**
- scientific diagnostic: **not started**
- run_execution_valid: False

The only error was again C206 test25. The semantic-count rewrite referenced `c205._iter_tests` and
`c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS`, but the test module imported only `c202` and `c206`.
Python compilation succeeds with such an unbound function-body name, so the error appeared only when
test25 executed:

```text
NameError: name 'c205' is not defined
```

### Recovery

No new import is required. test25 now uses the parent module binding that C206 itself actually uses:

```python
c206.c205._iter_tests(...)
c206.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
```

A remote alias audit after the change shows executable bare module references are limited to the
explicitly imported `c202` and `c206`; C171 names in test21 are string literals only.

### Process correction

Post-authoring review now includes a Python free-name/import-binding audit. New bare module aliases
introduced inside test/benchmark function bodies must resolve through an import or an already-bound
parent-module namespace. This specifically covers errors that `py_compile` cannot catch.
