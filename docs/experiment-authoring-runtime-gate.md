# Experiment authoring runtime gate

This document records the operational rule introduced after the C270 authoring-test incident.
It supplements, but does not replace, the experiment conversation handoff protocol.

## Why

C270's first formal invocation never reached regression or scientific evaluation. Own test23 used
AST call line numbers to assert phase order. Several valid phase calls shared one physical Python
line, so two different calls had the same lineno and the brittle test failed with `8 not less than 8`.
Static remote-byte review had checked the intended call ordering but had not executed the complete
own24 suite in the authoritative Windows repository. The experiment launcher therefore published
an INVALID log for an authoring/test defect.

## Mandatory rule for C270 and later experiments

Formal user launchers use two phases:

1. **Validate** — operational, before scientific logging or publication:
   - branch/tracked-tree/ExpectedHead/ACTIVE/parser/PowerShell guards;
   - Python compile/import checks owned by the experiment;
   - parent/source/artifact precheck;
   - complete experiment own-test module;
   - complete preregistered focused regression suite.
2. **Execute** — scientific, only after Validate returns PASS:
   - fixed model inference/training intervention;
   - checkpoint/output replay and persistence;
   - scientific postcheck;
   - console log publication.

A Validate failure is reported as
`invocation_skipped = AUTHORING_RUNTIME_PREFLIGHT_FAILED`,
`experiment_executed = False`, and
`execution_log_publish_attempted = False`.
It must not create/replace `docs/experiment-run-logs/c###/latest.*`.

After Validate passes, its text output is copied into the formal science log as an attestation so
the published evidence still records which own/regression checks passed. Execute must re-check
branch/tree/HEAD before science, but it need not repeat the expensive own/regression suite.

## Authoring-test design rule

Do not infer semantic phase order solely from `ast.Call.lineno` unless distinct-line placement is
itself the declared contract. Python permits multiple calls on one physical line.

For ordered scientific phases, prefer:
- one major phase call per physical source line; and
- exact source-call markers or AST statement/control-flow structure with uniqueness checks.

A call-order test must fail on reversed phase order, duplicate phase markers and missing phases.
Remote static review must inspect the exact assertion implementation, not just the intended result.

## Review status language

When the reviewer cannot execute the full committed own-test module and focused suite in a complete
checkout, describe the review as **committed-byte/static review PASS; runtime gate pending**.
Do not imply that authoring tests executed merely because their source was inspected.

The runtime Validate phase is the authoritative executable authoring gate. Only after it passes does
the invocation enter scientific execution/logging.

## Scope

This operational split does not change scientific data,weights,seeds,thresholds,model structure or
registered hypotheses. A failure during Execute after Validate is still a scientific/runtime
integrity failure and retries the SAME C number. A valid capability miss remains accepted evidence.
