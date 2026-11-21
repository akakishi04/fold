# C235 execution recovery — source-string false positive

## Formal status

**C235 INVALID EXECUTION / RETRY SAME C235.**
C235 remains the unique active experiment, in INVALID ATTEMPT RECOVERY.
C234 remains ACCEPTED VALID NEGATIVE; C236 is NOT REGISTERED.
Gate E remains PASSED; Gate F remains NOT PASSED.

This addendum supersedes the initial C235 readiness review for the retry. The original
preregistration remains the fixed scientific specification; no scientific condition is changed.

## Invalid attempt identity

Attempted scientific execution HEAD:
`d55e58f280bbd32776a6cd56ddc7507e6c827e1a`.

Published invalid-log commit:
`1615b5ce54afed8bde44ac9d326cace6c6e674d0`.

Log paths at that immutable commit:
- `docs/experiment-run-logs/c235/latest.log`
- `docs/experiment-run-logs/c235/latest.json`

Log SHA256:
`37834dbd3572d43a94ccd2372f6bc070cd8ffae3745f69975e38fe82c25fafd5`.
Log bytes: 9618.
The publication commit changed only these two log files. Retain this commit reference
when a later retry replaces the current latest files; do not discard the invalid evidence.

## Failure phase

Python syntax preflight PASS; source/artifact precheck PASS (256 source pins / 370 inputs).
Own authoring suite ran all 24 tests in 0.335s: 23 passed, 1 failed.
The failed test was:
`tests_lm.test_v05_c235_frozen_binding_diagnostic.C235Tests.test_22_run_is_frozen_no_training_or_checkpoint_write`.

The 2809-test focused regression and C235 scientific diagnostic were NOT started.
Tracked tree and execution HEAD were preserved. The log ends with
`run_execution_valid = False`. There is no C235 diagnostic result to accept or interpret.
Do not convert this authoring failure into an ability negative or a Gate decision.

## Root cause

The test applied `assertNotIn("optimizer", inspect.getsource(b.run))` to the entire function
source. The unchanged run function contains the result-limitation string:
`TRAIN scoring is not held-out generalization; no causal proof of optimizer/architecture cause`.

The test incorrectly treated a word in metadata as executable optimizer use. The earlier static
review missed this exact source-string false positive. The runner correctly stopped at the
own-test barrier; its stopping behavior is not the defect.

## Minimal repair and fixed boundaries

Code repair commit:
`a972c32c4b3de5e58ad3d9d3c0f7734256bafce7`.

Only the existing C235 test file changes: add the standard-library `ast` import and replace
raw forbidden-substring checks inside test_22 with executable-syntax inspection.
The checker inspects identifiers, attributes and calls, not comments/docstrings/string contents.
It rejects optimizer/optim references, fit/backward/step/zero_grad calls and torch.save references.
Existing requires_grad_(False) and parent EVAL replay checks remain.

The same test contains a harmless-text regression fixture and 11 forbidden-operation subtests.
These code snippets are parsed, never executed. The test is not skipped or removed.
All 24 test IDs remain; all other test method bodies are unchanged. No new historical exclusion.

No benchmark, runner, launcher, accepted parent source/test/log, model, dataset, split, seed,
threshold, replay tolerance, metric, manifest or production runtime is changed.
The original registered 120 modules / 2810 loaded / 2809 focused tests remain mandatory.
OWN6, 256 source pins, 370 protected inputs and the five output artifacts remain unchanged.

The retry still freezes all six accepted C234 step400 models, evaluates TRAIN384/EVAL192 under
three views, and performs 36 scientific forwards / 10368 row presentations / zero training.
C235 PASS still means diagnostic integrity only, never successful binding or Gate F completion.

## Independent post-authoring review

`post_authoring_review = PASS`

Review HEAD: `a972c32c4b3de5e58ad3d9d3c0f7734256bafce7`.
Scope: same-C repair review, with targeted local execution; NOT formal C235 acceptance.

After committing the repair, the remote test source was fetched again and its Git blob identity
was matched to the locally tested bytes:
- repaired tests: `570711dbce5080fed307ac2c67d027d685a8a3d8`
- unchanged benchmark: `12807b77a5f6bc36d185a931e54d651dcd557e39`
- unchanged runner: `f6debab11f8fb88c3519752626d6f4512ae3297d`
- unchanged launcher: `564359a1283a9bea333ce78611c085baa662d358`

Comparison from the invalid-log commit to review HEAD changes only the C235 test file.
The original benchmark/test copies were checked against their remote Git blob hashes before use.

Checks actually executed in the reviewer environment:
- original exact test_22 reproduced the published optimizer-string assertion failure;
- repaired exact test_22 passed against the unchanged actual b.run source;
- harmless comment/docstring/string fixture passed, while all 11 prohibited-operation controls
  were detected;
- Python py_compile of the complete benchmark and repaired test module passed;
- 17 fixture-independent test methods (01, 02, 04-07, 12-22) passed before and after the committed
  source readback; these were direct TestCase.run invocations, without the parent dataset
  setUpClass, and are NOT the full own suite;
- unittest's actual own-test loader still constructed 24 test cases;
- AST comparison found only test_22 changed among test methods; ast import binding was verified;
- manifest reconstruction remained
  `2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3`.

Reviewer environment: Python 3.13.5 / PyTorch 2.10.0+cpu / NumPy 2.3.5.
It is not the authoritative Windows Python 3.13.15 / PyTorch 2.10.0+cu130 environment.
The isolated container could not resolve github.com for a complete clone.

NOT executed by the reviewer: full 24-test suite with parent fixtures, the 2809 focused tests,
Windows PowerShell AST, accepted user-local artifact reads or the 36-forward diagnostic.
Do not label any of these pending checks PASS. The unchanged authoritative launcher/runner
must perform them, in their original order, on the retry.

## Retry and stop

Use tools/invoke_active.ps1 with the final recovery branch HEAD. Keep the outer dispatcher AST
preflight and existing branch/clean-tree/exact-HEAD/ACTIVE guards. Do not reuse the failed
ExpectedHead, bypass the own-test barrier or edit the benchmark explanation to hide the defect.

24 own tests -> 2809 focused tests -> C235 frozen diagnostic -> postcheck -> remote log publication.
A preflight, regression, schema, artifact, replay, nonfinite, mutation or protection failure stops
same C235. Transport-only failure is repaired without rerunning a completed scientific diagnostic.
No C236 registration, extra training, threshold rescue, cleanup or history rewrite.
