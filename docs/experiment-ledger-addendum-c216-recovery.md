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
`91e8afd97d667b67f1164e87628f62b4bcf2347e2884537ec3e54c2baa6b385c`

## Recovery review

`post_authoring_recovery_review = PENDING`

Retry C216 only after committed remote bytes are reviewed, including a successful construction of
the full inherited regression module list with restored `run_c167.ps1`.
