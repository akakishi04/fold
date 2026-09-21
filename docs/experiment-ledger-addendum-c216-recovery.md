# C216 execution recovery — historical regression runner restore

## Formal disposition

**C216 INVALID EXECUTION / RETRY SAME C216.**
**C217 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## Invalid attempt identity

Scientific execution HEAD:
`8b550a92ab8db94d4a5c8ad7da7dadac1609ad6b`

Published log commit:
`c8f24d453455f97389c2e0935339e379d2a98e47`

Log SHA256:
`7efe5c61f4d8b727124e6030d6a93752bc215a96ef236ba055dda7807ab7ff62`

## Failure phase

Passed:
- repository preflight;
- Python syntax preflight;
- accepted C215 source/artifact precheck.

Failed before loading focused tests:

```text
FileNotFoundError:
M:\asobiba\fold\tools\run_c167.ps1
```

The exception arose while the inherited regression-module chain reached
`gate_e_c178_visible_leaf_binding.regression_modules()`, which parses
`tools/run_c167.ps1` to recover the historical 51-module regression seed list.

The learned Reader pilot did **not** run.

`run_execution_valid = False`.

## Root cause

Post-C215 working-tree cleanup pruned `tools/run_c167.ps1` because it was not part of C215's 122
scientific source pins. That cleanup audit checked accepted source pins and historical test source,
but missed the runtime dependency inside historical `regression_modules()`.

This is a maintenance/execution-validity defect, not scientific evidence about Reader learning.

## Minimal recovery

Restore the exact pre-prune file from Git history:

```text
tools/run_c167.ps1
blob 7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789
```

Restore commit:
`99ac3a0dff5a653b66c50b55e4b4ee9fe5d9f0e8`

C216 additionally pins this file as a historical regression dependency so future precheck rejects
its deletion or modification.

Recovery changes:
- restore `tools/run_c167.ps1`;
- add its exact blob to C216 source/protection accounting;
- strengthen existing C216 test31 to assert the dependency identity;
- update registration accounting from129/135 to130/136;
- update only the manifest's execution-validity dependency declaration/hash.

Unchanged:
- Reader1->8->3,43 parameters;
-36-row dataset;
- TRAIN6 / EVAL3 factor-pair split;
- dataset SHA;
- seeds216001/216002/216003;
-400 steps per seed;
- optimizer/lr;
-1215 Reader-forward workload;
- fixed100% Reader accuracy gates;
- zero-readout1/3 control;
- Writer/Port Selector/Coverage boundaries;
- Gate F interpretation.

Updated manifest SHA:
`77d42cd12ce26e592b7e4798ba844e6a8147af4f3f45fc870fb48790b36cbdd7`

## Recovery review

post_authoring_recovery_review = PASS

review HEAD:
`a69385699fa616d209bb7a1352c8e94bbe241b08`

Recovery review verified:
- restored `tools/run_c167.ps1` blob exactly
  `7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789`;
- its historical module-list parser yields exactly51 unique test modules;
- C176/C177/C178 are the historical builders that directly read that file; sampled downstream
  regression builders only inherit/append modules and do not introduce another deleted-script dependency;
- Reader production source, C216 runner and C216 launcher are unchanged from the invalid scientific
  execution HEAD;
- the only C216 benchmark/test changes are execution-validity protection for the historical runner;
- C216 manifest hash independently recomputes to
  `77d42cd12ce26e592b7e4798ba844e6a8147af4f3f45fc870fb48790b36cbdd7`;
- deterministic Reader dataset SHA independently recomputes to
  `9ded8a1b17cf721407e5d28c9dd6350159d0a17721f39bf9b57a911b78aa3f61`;
- TRAIN/EVAL target counts remain [8,8,8] / [4,4,4];
- source/protection accounting is130/136;
- C216 test count remains36 and focused regression registration remains2185;
- complete PowerShell source contract remains unchanged and satisfied;
- C217 remains unregistered.

Scientific split, seeds, model, optimizer, training workload, thresholds and interpretation boundary
remain frozen.

Retry C216 only after committed remote bytes are reviewed, including a successful construction of
the full inherited regression module list with restored `run_c167.ps1`.


---

## Second invalid retry — dataset byte identity

Scientific execution HEAD:
`c7179ddeaed2e092d3f1f6090e9bd09a1ff9c75e`

Published log commit:
`cfdb0a89a7bf7d14ae1bf7b541f7722dd8adecb1`

Log SHA256:
`fb028f5c206e42603cab2dc14fcd2276b8c3f98e4416378bf8b65901256f097f`

Failure phase:
- repository preflight PASS;
- Python syntax preflight PASS;
- accepted C215 source/artifact precheck PASS;
- historical regression runner restored successfully;
- inherited C100-C215 regression tests reached2149 passed;
- C216 test class setup failed before its36 tests could execute;
- learned Reader training did not run;
- run_execution_valid False.

Failure:

```text
ValueError: C216 dataset content drift
```

Root cause:
the originally registered dataset SHA was calculated from the algebraically equivalent Python
expression `0.75 / 4.25`. The actual C216 dataset is generated through the accepted FOLD-R
`torch.linalg.solve` response-capsule path. For the nonzero scalar readout those paths differ by
one float64 ULP. Semantic values, pair membership, labels, placement and class balance are unchanged.

Actual FOLD-R selected-value bit patterns:

```text
-1 -> 13818898080148657814
 0 -> 0
+1 -> 4595526043293882006
```

Correct dataset SHA256:

`9ded8a1b17cf721407e5d28c9dd6350159d0a17721f39bf9b57a911b78aa3f61`

Correct manifest SHA256:

`77d42cd12ce26e592b7e4798ba844e6a8147af4f3f45fc870fb48790b36cbdd7`

Recovery:
- update DATA_SHA to the bytes actually produced by the preregistered FOLD-R numeric path;
- update manifest hash accordingly;
- strengthen existing test13 to assert the exact three float64 bit patterns.

Unchanged:
-36 rows /24 TRAIN /12 EVAL;
- TRAIN six pair combinations / EVAL three pair combinations;
- target balances [8,8,8] / [4,4,4];
- Reader1->8->3 /43 parameters;
- seeds216001/216002/216003;
- Adam lr0.02 /400 steps each;
-1215 Reader-forward accounting;
- all scientific accuracy/control thresholds;
- Writer/Port Selector/Coverage boundaries;
- Gate F interpretation.

`post_authoring_recovery_review_2 = PASS`

review HEAD:
`926979cdc19fab3b44c12869ed1b551b0b56f55a`

Second recovery review verified:
- actual FOLD-R `torch.linalg.solve` selected-value float64 bit patterns are exactly
  `13818898080148657814 / 0 / 4595526043293882006`;
- the deterministic 36-row dataset generated from that numeric path hashes to
  `9ded8a1b17cf721407e5d28c9dd6350159d0a17721f39bf9b57a911b78aa3f61`;
- TRAIN/EVAL target counts remain [8,8,8] / [4,4,4] and the six/three pair split is unchanged;
- the manifest independently recomputes to
  `77d42cd12ce26e592b7e4798ba844e6a8147af4f3f45fc870fb48790b36cbdd7`;
- benchmark source differs from the second-invalid execution version only in DATA_SHA and
  MANIFEST_SHA;
- production Reader source, C216 runner and C216 launcher are byte-identical to the
  second-invalid execution version;
- existing test13 now pins the exact float64 bit patterns; total C216 tests remain36;
- restored historical `tools/run_c167.ps1` remains exact blob
  `7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789` and yields51 unique seed modules;
- source/protection accounting remains130/136 and focused regression registration remains2185;
- complete PowerShell guard/source-string contract remains satisfied;
- C217 remains unregistered.

No split, seed, model architecture, optimizer, workload, threshold, or interpretation boundary
changed during recovery.
