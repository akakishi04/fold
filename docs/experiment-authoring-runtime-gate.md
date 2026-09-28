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


## Manifest sealing rule

Registration hashes are sealed only after the final committed scientific/authoring source is stable.

Before activation:
1. finish all benchmark/test/runner/launcher edits that can change `manifest()`;
2. compute `digest(manifest())` from the final committed benchmark source;
3. write that exact value into `MANIFEST_SHA`, preregistration and handoff;
4. re-fetch the committed benchmark and independently recompute the digest;
5. only then mark post-authoring review complete or update the experiment to ACTIVE.

Any edit to fields returned by `manifest()` invalidates the previous seal and requires steps2-4 again.

Runtime precheck must report actual source-pin count, actual protected-input count and actual manifest
digest before asserting them. Count mismatch and manifest mismatch must have separate error messages;
do not combine them into one generic `registration` failure.

Static review notes must quote the final committed manifest digest, not a value copied from an earlier
draft. If the reviewer cannot recompute it from final committed bytes, activation remains pending.


## Registration metadata single-source rule

Registration cardinalities such as `source_pins` and `protected_inputs` must have exactly one
executable source of truth: the final sealed `manifest()`.

Runtime validators and prechecks must derive expected counts from:
`manifest()["source_pins"]` and `manifest()["protected_inputs"]`.
Do not repeat numeric tuples such as `(478,826)` inside `validate_result`, `precheck`, or other
scientific Python validators.

Human-readable preregistration, runner output and handoff may repeat the numbers for review, but they
are descriptive copies. Tests must verify that executable validators read the manifest fields rather
than compare against separately hard-coded numbers.

When a count changes:
1. change the manifest field and structural arithmetic test;
2. update human-readable docs/output;
3. reseal the manifest because manifest content changed;
4. never separately patch a validator's numeric literal, because no such literal should exist.

This rule addresses the C272 preflight incident where protected_inputs was corrected from820 to826
in the manifest/precheck path while `validate_result` retained the stale820 literal.


## Mutable handoff lifecycle rule

The current handoff is mutable operational state. Accepted experiment tests must not unconditionally
require their experiment-specific activation text or manifest seal to remain in the current handoff
forever.

For C273 and later own tests:
- while that experiment is ACTIVE, the test may require its sealed manifest in the current handoff;
- after that experiment is no longer ACTIVE, the test must require the seal in the immutable
  acceptance addendum `docs/experiment-ledger-addendum-c###-c(next).md` instead;
- the test must determine this from the handoff Formal state rather than assuming one lifecycle phase.

If an older accepted/pinned test already unconditionally reads the mutable handoff and cannot be
edited without violating parent provenance, preserve the required value in an append-only
**Inherited regression compatibility seals** section of the handoff. Current known legacy entry:
- C272 manifest: `89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604`.

Every new experiment's own authoring tests must assert that all listed legacy compatibility seals
remain present in the handoff. This catches accidental removal during own24, before the several-minute
focused regression suite.

Before activation, static review must inspect inherited tests that read
`docs/experiment-ledger-and-handoff.md` and classify each dependency as:
1. active-only lifecycle-aware;
2. immutable acceptance-addendum based; or
3. legacy compatibility seal that must be retained.

Do not add a new regression exclusion to work around mutable-handoff failures.


## Multi-parent fixture fidelity rule

When an experiment verifies more than one parent summary or provenance root, authoring tests must
model those parent identities independently. A single constant-return hash mock must not stand in
for multiple required parent hashes.

For every multi-parent `load_parent(...)` path:
1. enumerate each parent input and its registered SHA separately;
2. make the test double return the SHA by input identity/path, not by one global constant;
3. assert that the loader actually queried each expected parent input;
4. include a negative test where one secondary parent returns the wrong SHA and require the loader
   to fail before any scientific work;
5. if a parent verifier receives different argument roles (e.g. parent run directory vs ancestor
   summary), preserve those roles in the test fixture instead of collapsing them.

Static post-authoring review must compare the number of independently registered parent hashes in
the benchmark with the number of independently modeled parent hashes in the corresponding own test.
If the benchmark has N distinct parent hashes and the fixture only models fewer than N identities,
activation remains pending.

This rule addresses the C276 preflight incident where the real loader correctly required distinct
C275 and C274 summary hashes,while own test16 used one constant hash for both inputs and therefore
failed before science.
