# C189 execution recovery — corrupted source blob

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

## Formal status

**C189 remains ACTIVE / NOT YET JUDGED.**
The first C189 attempt is **INVALID EXECUTION / RETRY SAME C189**.
C190 remains NOT REGISTERED. Gate E remains NOT PASSED.

Invalid attempt:
- scientific execution HEAD: `8733da67f8fee522d4deb2417c942ac734b582a9`
- published log commit: `a7fe8158df96f41541579be4f35722daf81e6687`
- published log path: `docs/experiment-run-logs/c189/latest.log`
- log SHA256: `3bf74d001b1ec24cc202df77a9ab7ebe3ff5f17ff4122aafd3b643d5d0d7a5b2`
- log bytes: 907
- focused benchmark work: **not started**
- failure phase: source/artifact precheck import
- exception: `SyntaxError: source code string cannot contain null bytes`

The Python source blob registered for
`fold_lm/v05_benchmarks/gate_e_c189_live_multimissing_target.py` was malformed:
it contained NUL / non-UTF-8 bytes. This is an implementation/serialization failure,
not scientific evidence about the candidate.

## Recovery

Replace only the malformed C189 benchmark source with a valid UTF-8 implementation of
the already preregistered C189 contract.

Unchanged:
- experiment ID/stage;
- C188 parent/result;
- all C181/C188 checkpoint identities;
- cohort 1768 / discriminating528;
- 9 selectors x2 source bits = 18 blocks /31824 episodes;
- one shared initial base forward for necessity+target;
- one real RETRIEVE maximum;
- one post necessity decision;
- no second acquisition;
- source fixtures;
- scoring teachers;
- workload expectations;
- strict gate;
- scientific manifest SHA256
  `6acccb0b116a57a34e4f91733d0a15ac345d144ba9b6cb0db8a1e7af4ecf0e47`.

No threshold, seed, data, model width, training budget or interpretation is changed.

The already-published invalid log remains in history. On retry,
`docs/experiment-run-logs/c189/latest.log` / `latest.json` are replaced by the new
run's dedicated log commit while the old invalid log remains recoverable from commit
`a7fe8158df96f41541579be4f35722daf81e6687`.

Retry SAME C189 only. Do not register C190 before C189 judgment.

## Second invalid attempt — manifest hash transcription

Retry execution HEAD: `e8e09e267d686427f2e3381e171e9f54b34533f6`.
Published log commit: `0f0594ddb9dd0a607451318d7ba33a6ecd061a7e`.
Log SHA256: `438ebe247d303d555719b679208e99d11224aae4d556182af4b8dd5d80ce6bca`.
Log bytes: 1339.

The UTF-8 source imported successfully and all inherited source/artifact checks reached the
scientific-manifest guard. It then stopped with `ValueError: Manifest drift` before focused
regression or model inference. Recomputing the exact canonical manifest object yields
`e1ba8c1b84dc016410e91432eadfc53e28a46dd49cb91bf015d3336f37e8402e`.
The old fixed SHA was incorrect; no manifest field or scientific condition is changed.
C189 remains ACTIVE / NOT YET JUDGED; retry SAME C189.

## Third invalid attempt — test fixture epoch mismatch

Retry execution HEAD: `5af67ef5e9b71a640f0787877af2e8cd7bb5ca2d`.
Published log commit: `1da20c1db1f3127be3070c4f76088b7292fe7426`.
Log SHA256: `c2e8f17ed9b5ab934dc525707c6a70bf67c4141717ff5a174f60dcc90365090e`.
Log bytes: 239417.

This attempt passed source/artifact precheck and entered the full focused regression.
Existing historical tests and 30/36 new C189 tests passed, but six C189 acquisition tests
failed before the benchmark ran. The failure was localized to the synthetic C189 unit-test
helper `raw_row()`: it left structured-input header coordinates evidence_time/revision at
0/0, while the real C174 source rows and registered C185-format providers use epoch 1/1.
C173 therefore correctly rejected synthetic dispatches as SOURCE_EPOCH_MISMATCH before
provider invocation, causing zero provider reads and one fewer internal charge.

Recovery changes only the synthetic test fixture to encode evidence_time=1 and revision=1,
matching the actual C174 TaskView contract. The benchmark source, scientific manifest,
seeds, checkpoints, cohort, workload, gate, thresholds and interpretation are unchanged.
C189 remains ACTIVE / NOT YET JUDGED. Retry SAME C189; C190 remains unregistered.
