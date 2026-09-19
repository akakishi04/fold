# C195 execution recovery

## First invalid attempt — unit reference fixture rank mismatch

Execution HEAD: `33da93a7e227799988cad0762b1d73e6cdefe92f`
Published log commit: `f216c5f701799516a152025f3be8c3d1b08f220e`
Log SHA256: `67597c92c4b7b3e738424bc29ad242f71cd072152dc530b0d821508237d4f7ff`.

Source/artifact precheck passed. All **1605** focused tests ran; exactly two C195 unit tests
errored before benchmark execution:

- `test_11_reference_replay_exact`
- `test_12_replay_detects_unauthorized_final`

Root cause:
the synthetic helper `three_need_reference()` returned one episode without its leading batch
dimension:

```text
necessity_predictions [3]
necessity_logits      [3,2]
target_predictions    [3]
target_logits         [3,4]
```

while the real accepted C191 artifact and `reference_replay_metrics()` contract are batched:

```text
[N,3]
[N,3,2]
[N,3]
[N,3,4]
```

The production benchmark path therefore was not exercised and no scientific model evidence
was produced.

Recovery changes only the test fixture to the one-row batched shapes `[1,3,...]`.
Benchmark source, manifest, gate, C191 reference identity, budget12 condition, seeds,
checkpoints, cohort, worlds and interpretation are unchanged.

C195 remains **ACTIVE / NOT YET JUDGED**. Retry SAME C195. C196 remains unregistered.
