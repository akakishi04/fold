# C186 execution recovery — accepted C185 NPZ exceeds the inherited size ceiling

V5-E; repository `akakishi04/fold`; branch `feat/sft-target-loss`.

## 1. Formal disposition

**Attempt at a4127d8a6bef0bf7eafd6e5d76fbb2061ab74eba: INVALID EXECUTION / RETRY SAME C186.**
C186 remains **ACTIVE / NOT YET JUDGED** scientifically. This is not a valid negative.
C185 remains ACCEPTED PASS; all earlier judgments/checkpoints remain unchanged.
**Gate E NOT PASSED. C187 NOT REGISTERED.**

The original `docs/experiment-ledger-addendum-c186-preregistration.md` stays unchanged.
This addendum records an execution-only repair, not a replacement scientific protocol.

## 2. Observed execution and evidence

Uploaded log: `貼り付けられたテキスト（1 点）(20260918-151856).txt`.
218,511 bytes; SHA256:
`2772bdf9cc8f0e28fa769a6f10d6c9c950860e790ddc49ce554555db665ea1a0`.

Source/artifact precheck PASS. **1,317 / 1,317 tests PASS in 40.601 s.**
The benchmark then stops at C186 `run`, original line 316, while opening the
already accepted C185 `episode-predictions.npz` through C175 `audit.load_npz`.
Error: **`InvalidExecution: Oversized expanded NPZ`**.
Postcheck: protected inputs preserved, tracked tree clean, execution HEAD preserved,
`run_execution_valid = False`.

Source order places this error BEFORE checkpoint restoration, static model replay,
provider construction and all 80 episode blocks. There is no C186 RESULT/summary in
the supplied log and zero completed episode blocks. No new-condition predictions,
acquisitions or learning occurred in this formal benchmark attempt. Unit-test work
must not be counted as formal experiment activity. `invalid.json` is written by the
exception handler, but its separate bytes/output-directory identity were not supplied.
Preserve that failed run directory and the uploaded log; do not overwrite or delete them.

## 3. Cause — file-shape contract, not model performance

C175's generic loader caps the ZIP sum of uncompressed member sizes at
33,554,432 bytes (32 MiB). Its original small prediction arrays fit that contract.
The C185 producer stores eight arrays, including all per-episode/phase numeric inputs.
Their registered shapes imply the following raw payload sizes, before NPY headers:

|Array|Shape|dtype|Payload bytes|
|---|---|---|---:|
|predictions|8,2,2,3712,2|int8|237568|
|logits|8,2,2,3712,2,2|float32|1900544|
|logit_present|8,2,2,3712,2|bool|237568|
|policy_inputs|8,2,2,3712,2,72|int32|68419584|
|row_indices|3712|int32|14848|
|policy_seeds|8|int32|32|
|policy_names|8|Unicode18|576|
|layouts|2,4|int8|8|
|Total|||**70810728**|

That is approximately **67.53 MiB** of array payload, not a measured whole-process
RAM figure. `policy_inputs` alone already exceeds 32 MiB. Compression on disk does
not change the expanded-size guard.

Accepted C185 summary SHA256:
`843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949`.
Its `episode-predictions.npz` is 1,716,066 serialized bytes with SHA256:
`e597baf0dfa76b34a32dcb2a0445640aaeb21bb99a22af25c26c854ef3eabcf8`.
The complete C185 log supplies this artifact identity; the actual NPZ was not uploaded.
This failure is not evidence that the accepted file is corrupt or must be regenerated.

## 4. Bounded repair and held-constant conditions

Add `fold_lm/v05_benchmarks/c186_c185_npz_input.py`. Only C186 uses it to read this
C185 artifact. **Do not edit/monkeypatch C175 or increase its generic 32 MiB limit.**
The new public reader exposes no caller-set hash, size ceiling, unsafe-pickle option,
case filter or prediction-repair switch.

The reader verifies the accepted compressed size and SHA256, exact eight member
names, no duplicates/directories/encryption, registered dtypes and shapes, C order,
and exact NPY header-plus-payload lengths. It inspects ALL headers before allocating
arrays. NPY v1/v2 header text is bounded at 4,096 bytes/member. The total expanded
ceiling is schema-derived: **70,843,592 bytes**, including framing/header allowance.
Object/structured/unregistered dtypes, oversized shapes, malformed headers and trailing
payload are rejected. Arrays are read with `allow_pickle=False`. One open descriptor
is used for hash/schema/materialization and the file is rehashed afterwards.

C186 precheck now validates this archive's headers BEFORE the regression suite.
The benchmark's one C185 NPZ load uses the new reader; all saved fields/values still
feed the existing exact row/policy/layout and replay checks. No alternate data or
model execution is substituted. The runner prints the new schema check and output path.

Unchanged: cohort, all six C181 checkpoints/seeds, both rule controls, five scenarios,
80 blocks / 296,960 episodes, budgets, injected outcomes, labels, model input/preparation,
argmax, 1e-6 replay tolerance, finite-failure gate, no training/teacher/auxiliary head,
C185 driver and C170/C172/C173 runtime. Scientific manifest SHA256 remains exactly:
`0cbe7212e5bafd9fc52f3f315d2d4732afaca6eb11940c6fa16ac58aeb336edc`.

Bookkeeping changes only: 24 recovery tests added; **1,341 expected tests = 1,317 + 24**,
71 modules. The loader, its test module and this addendum join C186 OWN, so protected
input paths become **203 instead of 200**, while historical source pins remain **92**.
The original preregistration's historical counts stay visible; this addendum records
these current execution counts. Scientific output artifact set stays 13.

## 5. Validation completed and limits

Reviewer reconstructed the original complete C186 module and runner from GitHub;
Git blob hashes matched `00bbf35c70ffa1c9afcb927fba829bae8e408321` and
`f76130b33de4eca4f0273fa024c577b582ba1ef2` before patching. The unmodified existing
32-test module matched blob `eeda2a782bafdbeab07fb929ebefff7a8067962b`.

**56 / 56 local helper tests PASS**: the unchanged 32 C186 tests plus 24 new recovery
tests, on the actual complete patched C186 module and complete new loader.
A synthetic NPZ with ALL registered shapes/dtypes and the full 70,810,728-byte payload
was generated, accepted through a test-only patched file identity, loaded and compared
array-for-array. It reproduces the old expanded-size exceedance; every loaded element,
dtype and shape remains unchanged. Header-only precheck was tested without array loading.
Malformed/duplicate/oversized/object/shape/order/identity cases reject; public production
constants never point to synthetic data. The fixed C186 manifest hash is tested unchanged.
The benchmark functions for scenario generation, injection, score_episode, gate and
replay tolerance are unchanged; no runtime/model computation is used by loader tests.

Python compilation and all three runner-embedded Python blocks pass syntax checks.
No full Git checkout was available (local Git DNS lookup failed). **Full 1,341-test
regression, Windows PowerShell, actual accepted NPZ bytes, the complete 203-input chain,
and all formal C186 predictions/episodes remain unexecuted here.** No new scientific
scores are known and no success beyond the tested reader contract is claimed.

## 6. Retry / stop

Fast-forward the same branch to this repair commit. Do not reset/rebase, rebuild C185,
regenerate checkpoints, delete artifacts or edit old summary commit_sha values.
Archive the old console log, use the SAME eleven parent summaries, and run
`tools/run_c186.ps1` with the repaired ExpectedHead. A new GUID output directory
preserves the INVALID attempt. If scientific failure occurs, collect the whole run
without changing cases, thresholds or checkpoints. **No C187 before C186 judgment.**
