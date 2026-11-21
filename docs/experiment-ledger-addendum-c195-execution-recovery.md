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


## Second invalid attempt — C191 summary record field-name mismatch

Execution HEAD: `4cfa9238d335f734a58cb602baa7edf369eeb6b6`
Published log commit: `10685a707d4d80dde4a4732fca14d3cf4a2237d3`
Log SHA256: `ddccd960551ac9f71c6d92c6ed8b483ac37ff77b257208e222ce0ebb9f85be82`.

This retry passed **1605/1605** focused tests and entered the benchmark. It then stopped after
the first generic-loop block, before any formal C195 result, with:

`KeyError: 'second_provider_calls'`

A full schema audit against the accepted C191 RESULT shows the actual per-block record keys are:
- `parent_second_reads`
- `third_provider_calls`
- `parent_final_needs`
- `actual_reads`
- plus C191 boundary/status counters.

C195 had incorrectly guessed two nonexistent aliases:
- `second_provider_calls`
- `final_needs`

Recovery:
- introduce `reference_block_expectations(ref_rec)` as the sole C191 record-schema adapter;
- validate required keys, integer counters, episodes9536, exhausted/third count928, final logical
  NEEDS0 and fourth-decision-accepted0;
- map C195 second reads from `parent_second_reads`;
- map third/exhausted rows from actual `third_provider_calls`;
- keep `actual_reads` direct through the adapter;
- strengthen the existing source-level test to reject the nonexistent aliases.

No model/runtime science changes: generic C194 loop, budget12, C191 NPZ reference,
manifest, seeds, checkpoints, cohort, source worlds and gate semantics are unchanged.

C195 remains **ACTIVE / NOT YET JUDGED**. Retry SAME C195. C196 remains unregistered.
