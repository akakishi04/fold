# C203 execution recovery — regression source-audit mismatch

## Disposition

**C203 — INVALID EXECUTION / RETRY SAME C203.**
**C204 NOT REGISTERED.**
Gate E remains **NOT PASSED**.

Invalid execution:
- execution HEAD: `13b1db0c595f6d4900a038693f6c0d87728e3996`
- published log commit: `c437165ea115592fa6449791b62419f5ce0bb4ad`
- log SHA256: `cb59ebfadd11bbee559861ce38dddca027af9b3c28e93e08da619a7d3a658371`
- focused regression: **1813 tests, 1812 PASS / 1 FAIL**
- scientific diagnostic: **not started**
- run_execution_valid: False

## Failure phase

Passed:
- repository preflight;
- Python syntax preflight;
- source/artifact precheck;
- 1812 regression tests.

Failed:
`tests_lm.test_v05_c203_mixed_channel_multistep_replay.C203Tests.test_22_source_replay_uses_saved_predictions`

The benchmark workload did not run.

## Root cause

The test intended to prove that C203 uses accepted saved C199 predictions rather than live model
inference.

The actual implementation correctly performs the artifact lookup in the caller:

```python
collect(...)
    -> predictions["necessity_predictions"]
    -> predictions["target_predictions"]
    -> replay_block(..., necessity, targets, ...)
```

But the test asserted that the literal string
`predictions["necessity_predictions"]`
must occur inside `replay_block()`, where the arrays have already been passed as the parameters
`necessity` and `targets`.

This is an authoring-test target mismatch, not a runtime or scientific failure.

## Why this escaped post-authoring review

The previous post-authoring review verified:
- test count;
- manifest;
- parent identities;
- runner and launcher wiring;
- presence of source-level replay tests;
- decision/action ordering.

It did **not** mechanically evaluate each `inspect.getsource()` string assertion against the exact
function source it inspected. The review therefore confirmed the existence of test22 but did not
catch that one assertion mixed the caller variable namespace with the callee function.

## Minimal recovery

Change only test22:

- inspect `collect()` for direct reads of
  `predictions["necessity_predictions"]` and `predictions["target_predictions"]`;
- inspect `replay_block()` for use of `necessity[i,phase]` and `targets[i,phase]`;
- continue rejecting `combined_predict` / `necessity_predict` in the replay path.

Unchanged:
- C203 scientific question;
- accepted parent identities;
- fixed channel layout;
- fixed 214948 decision /129124 acquisition /85824 final-SUFFICIENT totals;
- source/protected/artifact counts;
- manifest SHA;
- PASS/FAIL gate;
- regression count1813;
- production runtime scope.

## Process correction

The post-authoring review protocol now explicitly requires mechanical cross-checking of
`inspect.getsource()` / source-string assertions against the exact inspected function, including
caller/callee ownership of expected strings.

C203 must pass the revised post-authoring review before the retry command is issued.
