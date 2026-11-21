# C324 R2 post-authoring review - bounded native diagnostic

post_authoring_review = PASS
Review target HEAD: 8f7fec8371cfa5792b89587fa078ff2b6aab80fb.
Review date: 2026-10-15.
Scope: operational recovery diagnostic ONLY; not a fix certification for the native
crash, not scientific execution validity, not C324 capability, not C325 registration.

## Remote-byte review

After committing the implementation, the complete Python controller (two consecutive
ranges), complete test file, complete C324 launcher and complete R2 launcher were
fetched again from the immutable target HEAD and reread. Their Git blobs equal the
independently computed hashes of the locally tested raw bytes:

| File | Git blob |
|---|---|
| tools/c324_native_diagnostic_r2.py | 30fba0cc27e571a2866e6015e63c2303cfe271ab |
| tests_tools/test_c324_native_diagnostic_r2.py | 398663c230f22482628f57acd8f54e433a5c4f21 |
| tools/invoke_c324_native_diagnostic_r2.ps1 | 6d2c370ee98b97fd74d8481fc978ac64d9e3e69b |
| tools/invoke_c324.ps1 | 45ecdff40ba9b672026003eae5157d704af6a7f2 |

Both Python files compile and decode as UTF-8 without NUL. A symtable free-global
binding audit found no unresolved globals. Source assertions inspect the exact
worker function, not a caller. Tests and controller have no import-time training.
The old launcher was independently reconstructed and matched its original
cc92a0e6efe8c4b203a1d81a03faa45f9725fea0 blob before inserting the recovery block.
The compare shows only10 lines added to that existing launcher. Its50 parent paths,
normal scientific body and protected shared dispatchers remain unchanged.

## Tests actually completed after matching remote blobs

Environment: Linux, Python3.13.5, PyTorch2.10.0+cpu. Scientific data unavailable.
Authoring tests executed as three explicit partitions, not the full scientific suite:
- test01..24:24 run, failures0/errors0,3.530s.
- test25 healthy import fixture:1 run, failures0/errors0,20.130s.
- test26 stale-cache fixture:1 run, failures0/errors0,15.651s.
Total26 distinct tests passed. The two integration tests launch actual interpreter
processes and import actual PyTorch/NumPy but use synthetic repository modules.
The stale fixture intentionally retains a valid old pyc timestamp/size while changing
an equal-length function docstring. The existing-cache worker detects the differing
code signature; the empty-prefix worker reads the current source and passes. Original
source/cache bytes are preserved. This does NOT reproduce the user's native fatal.
Earlier attempts to run all26 within a single container command timed out at the
container boundary and are not claimed as full-suite successes. The completed
partitions above are the evidence for this review.

Covered:non-executing source compilation,code-signature differences,cache preservation,
no-overwrite,scope/HEAD/source guards,selected environment-only reporting,actual
subprocess failure/timeout capture,exit0 without a receipt rejection,two-outcome
aggregation and no automatic science,launcher publication/preflight ordering.

## Execution-path review

The active dispatcher parses invoke_c324.ps1. Its invalid-recovery branch validates
the registered recovery_action, parses the R2 launcher, invokes it and returns before
the scientific runner. The R2 launcher repeats branch/HEAD/tracked-tree/recovery guards
before log creation. It uses only the fixed authoritative venv executable and the
tracked diagnostic script. The Python controller rechecks source/HEAD before/after.
No new executable HEAD may be inferred from a historical log or mutable branch guess.

Each worker has a120-second bound, stdout/stderr files and10-second heartbeat;
exactly two outcomes are collected without retrying a scientific task. Existing
cache remains untouched. -B alone is not presented as disabling cache reads; the
fresh variant additionally uses a new empty pycache_prefix. Both use the same
interpreter, precision/thread setup and scientific files; no -O/-I/GIL override.
The controller forbids a scientific status PASS and always stops for review.
The diagnostic publisher is transport only and prints the explicit diagnostic role.

PowerShell is not installed in the authoring Linux container. No Windows AST or
end-to-end Windows execution is claimed. The executable path requires ParseFile for
the dispatcher, selected launcher and R2 launcher before invocation; reviewed scripts
are ASCII. The original Windows50-parent/full5357 run is not repeated or waived here.

## Evidence and non-claims

Published C324 failed log/metadata blobs are copied unchanged into an immutable
attempt directory; the old handoff is archived. No C323/earlier accepted source,
model, dataset, checkpoint, threshold, seed, scientific manifest or test was edited.
The current recovered state is INVALID ATTEMPT RECOVERY and diagnostic-only.
A short-probe success cannot establish that the complete native crash is fixed.
The full5357 suite and protected-input checks remain required for a later science
retry, with any safe performance work separately validated and disclosed.
