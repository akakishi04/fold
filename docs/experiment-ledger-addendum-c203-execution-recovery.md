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

## Revised-review finding before retry

After fixing the caller/callee mismatch, the strengthened mechanical review caught a second
latent false positive **before** another user execution:

```python
self.assertNotIn("necessity_predict", collect_source + replay_source)
```

This substring also matches the valid artifact key name `necessity_predictions`. The guard was
therefore narrowed to actual call syntax:

```python
"necessity_predict("
"combined_predict("
```

The revised committed source audit now verifies mechanically that:
- `collect()` contains both accepted artifact reads;
- `replay_block()` consumes the sliced `necessity` / `targets` parameters;
- neither replay path contains live `combined_predict(` or `necessity_predict(` calls;
- decision charge precedes the temporary authority window;
- dispatch precedes parent-authority restoration.

No scientific condition changed.

## Second invalid attempt — parent artifact semantic adapter

Disposition: **INVALID EXECUTION / RETRY SAME C203**.

- execution HEAD: `fad0c9df501e38159dfe77b746c63456534024c4`
- published log commit: `529c081e898eb75a68eccf99113c49ff7aa6b681`
- log SHA256: `11bca2741e2d5a36dd9ebd2e834307f057babb7fca65b00405d35f69727d1277`
- focused regression: **1813/1813 PASS**
- C203 block progress records: **0**
- scientific provider calls/publications: **0**
- run_execution_valid: False

Failure occurred at the first parent-artifact projection before any C203 acquisition dispatch:

```text
ValueError: Accepted target/decision depth mismatch
```

### Root cause

C203 treated every nonnegative entry of the accepted C199 `target_predictions` array as an
executed acquisition target.

That interpretation is wrong. C199 writes target-head outputs for every active row whenever
`any_missing` is true for the active batch, **before** checking that row's necessity decision.
Therefore a row whose necessity is `SUFFICIENT(0)` can still have a nonnegative target prediction
stored at that terminal phase. That target was computed but never acted on.

C199 action gating is:

```text
save necessity/target prediction
if necessity == SUFFICIENT:
    stop; target is unused
else:
    validate target
    acquire target
```

The accepted parent totals prove the action semantics:

```text
first acquisitions   85824
second acquisitions  34948
third acquisitions    8352
---------------------------
total acquisitions  129124

decisions           214948
final SUFFICIENT      85824
```

### Minimal recovery

C203 projection now derives acquisition depth from `necessity == NEEDS(1)`, not from
`target_predictions >= 0`.

For each replayed phase:
- necessity0: stop; ignore any stored target-head output at that phase;
- necessity1: require the corresponding target slot and project/execute that target.

Final per-episode reference acquisition count is likewise the number of accepted NEEDS decisions.

The C203 unit fixture now deliberately includes a nonnegative target prediction on a terminal
SUFFICIENT phase, matching C199 writer semantics. Existing projection-count tests therefore catch
this semantic mistake.

Unchanged:
- C203 scientific question;
- fixed fact-to-channel layout;
- accepted C199/C202/C174 identities;
- decisions214948 / acquisitions129124 / final-SUFFICIENT85824 fixed totals;
- manifest SHA;
- gate/workload;
- production runtime scope.

### Process correction

Parent artifact review now includes **writer-side semantics**, not only key names, dtype and shape.
For prediction artifacts, review must distinguish "prediction was computed/stored" from
"prediction passed the parent action gate and was executed". Child depth/count/projection adapters
must reproduce the parent gating semantics from the writer source.
