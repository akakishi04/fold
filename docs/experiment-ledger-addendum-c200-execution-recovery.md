# C200 execution recovery

## First invalid attempt — source-text import guard false positive

- execution HEAD: `4334bf492fe4d98e22165bb785edf3bcc9def254`
- published log commit: `3016e13924cc9ead8730c67401cd2d1969d2f339`
- log SHA256: `218adb7bbec8fa122b7ab591f2426e14200e98bc3d2f80e9c7c34552d81dfb1a`
- disposition: **INVALID EXECUTION / RETRY SAME C200**

Failure phase:

```text
authoring syntax preflight PASS
source/artifact precheck PASS
focused regression started
1730 tests PASS
1 test FAIL
scientific diagnostic did not start
```

Failing test:

`tests_lm.test_v05_c200_acquisition_channel_input.C200Tests.test_29_source_has_no_action_execution_import`

Root cause:

The test used `inspect.getsource(v2)` followed by raw substring rejection for
`structured_action_runtime` / `structured_acquisition_lifecycle`. The v2 module did not import
either module, but its explanatory module docstring mentioned
`structured_action_runtime`, causing a false positive.

This is an authoring/test bug, not scientific evidence and not a C200 negative result.

## Minimal recovery

Change only the import-guard test:
- parse the committed v2 module source with Python AST;
- inspect only `Import` / `ImportFrom` nodes;
- reject actual imports of action/acquisition runtime modules;
- allow explanatory docstrings/comments to mention the runtime boundary.

Unchanged:
- C200 scientific question;
- v2 schema/layout;
- 72+12 feature contract;
- diagnostic groups and counts;
- manifest SHA;
- parent C199 identity;
- PASS/FAIL gate;
- regression count1731;
- module count85;
- source/protected counts;
- production runtime scope.

C201 remains unregistered until C200 is formally judged.

## Process correction

The experiment-authoring protocol now requires a separate **post-authoring review pass** after
all source/tests/runner/launcher/preregistration files are written. The review must re-fetch the
committed remote bytes and re-check assertions, paths, counts, indexes, manifests and stale
copy/paste state before an execution command is given to the user.

C200 will not be re-issued until that review passes.
