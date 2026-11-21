# C270 execution recovery — own-test ordering assertion

## Formal state

C270 INVALID ATTEMPT / RETRY SAME C270.
C271 is not registered. C269 remains ACCEPTED PASS in its bounded scope.
Gate F NOT PASSED.

Invalid scientific execution HEAD:11ae165db9dbb73239360a20c9c7cf005cd9c19f.
Invalid log publication commit:9d5fca7390b767cc39c001792e9e478f43e8f96e.
Publisher log SHA256:3de30cc6d5d66d97d234e8068a931d5ae74b9d8782e65a3b9594448aca2a7de4.
Publisher log bytes:5560.
The log reaches parent/source/artifact precheck PASS and then stops in own test23.
No focused regression or C270 model evaluation ran. run_execution_valid=False.
There is no C270 capability result to judge.

## Failure phase and root cause

tests_lm.test_v05_c270_frozen_triple_identifiers.C270Tests.test_23_runner_cli_and_call_order failed:
AssertionError:8 not less than8.

The scientific run function called the intended phases in the correct semantic order, but several
major calls were compressed onto the same physical Python source line with semicolons. Test23 used
AST Call.lineno and required strict numeric line increase. Two distinct correctly ordered calls
therefore had the same lineno. This is a brittle authoring test, not a model/science failure.

The pre-activation review had statically inspected intended ordering but did not execute the complete
own24 suite in the authoritative Windows checkout. Calling that review PASS without an explicit
runtime-pending operational gate allowed an authoring-test defect to reach the formal log.

## Minimal scientific repair

Scientific data,three name profiles,parent C269 states,model architecture,scoring thresholds and
all frozen-transfer semantics remain unchanged.

Repair:
- format C270.run so major scientific phases occupy separate physical lines;
- replace lineno-only ordering with exact unique source phase markers and textual source offsets;
- require those markers to appear exactly once and on distinct lines;
- add launcher/runner tests for the new pre-science runtime gate.

No dataset/hash/gate/seed/profile/model change is authorized by this repair.

## Operational change for C270 and future C experiments

Adopt docs/experiment-authoring-runtime-gate.md.

The user-facing launcher now has two phases in one command:

1. Mode Validate, BEFORE formal science logging:
   Python compile, parent/source/artifact precheck, complete own-test module and complete focused
   regression. Output is stored in runs/c270-preflight-last.log.
   Any failure returns AUTHORING_RUNTIME_PREFLIGHT_FAILED with experiment_executed=False and
   execution_log_publish_attempted=False. It must not replace latest scientific logs.
2. Mode Execute, entered only after Validate PASS:
   the preflight transcript is copied into the formal log, then the fixed frozen C270 evaluation,
   replay and persisted postcheck run. No own/regression suite is repeated.

This would have prevented both the C268 protected-input incident and the present C270 own-test
incident from being classified/published as scientific execution failures. Runtime integrity errors
after Execute begins still remain SAME-C INVALID scientific attempts.

For authoring tests, AST lineno alone is no longer accepted as a semantic phase-order proof unless
distinct physical lines are themselves the declared invariant. Major phase calls should be one per
source line and tests should use unique exact source markers or structural statement order.

## Review boundary

A static committed-byte review without a complete checkout must be described as static PASS with
runtime gate pending. The authoritative executable authoring gate is Mode Validate on the user's
Windows repository. Do not claim own/full regression execution when only source inspection occurred.

C270 remains the only ACTIVE experiment. After repaired committed-byte review,activate a new C270
recovery HEAD and retry through tools/invoke_active_v2.ps1. Do not register C271 until a valid C270
result is judged.
