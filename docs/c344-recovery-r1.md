# C344 R1 — timeout後の一時ログ解放確認

Date: 2026-11-22 Japan time.
**C344 — INVALID EXECUTION / RETRY SAME C344.**
Same experiment `C344-v5b-pair-max-training` / stage `V5-B-PAIR-MAX-TRAINING`.
C343 remains ACCEPTED PASS (DIAGNOSTIC INTEGRITY); C342 remains ACCEPTED VALID NEGATIVE.
Gate F remains NOT PASSED. C345 is not registered.

## 1. Attempt 01 and evidence identity

| Item | Value |
|---|---|
| Scientific execution HEAD | `94fca46cfb31fcbb842997809012a1a692f7c45d` |
| Published log commit | `8d83d94b7923c0ebb06c052ee473c003cd490335` |
| Publication parent | Execution HEAD, sole parent |
| Original Windows log | 210,896 bytes |
| Original SHA256 | `6c3acf378c29567f1b83cba4184ff2df48788a42cf9c03bf55977281184553ec` |
| Git LF log | 208,199 bytes; 2,697 LF characters |
| Git LF SHA256 | `aa179488649bf5bf37ae31fdec7119d682177bd6212f39d8818a5c9d8151c835` |
| Git log blob | `e7407247a30f16f9910bffa5e34533088e2a787c` |
| Git metadata blob | `506f4ea430b36217228842efee9e2b2e7de2f2f9` |

Restoring CRLF exactly reproduces the metadata size and SHA256. Log publication
succeeded; this is not a transport failure. The publication added only latest.log
and latest.json. Exact Git copies are retained under
`docs/experiment-run-logs/c344/attempt-01/`; the original local run must also be retained.
The pre-recovery handoff is `docs/handoff-history/c344-pre-recovery-r1.md`.

## 2. Failure phase

Completed:

- Native read-lock probe.
- Parent C343 semantic verification, including its 483 retained outputs and 6,442-test evidence.
- Registration of 930 sources / 8,183 inputs and the original C344 manifest.
- C344 native numerical preflight: 16 forwards / 64 rows / 8 backwards / 0 optimizer updates.
- Regression modules 0 through 209: 210 complete modules / 5,357 successful tests.

Module index 210, `tests_tools.test_c324_locked_hash_r4`, ran 37 tests and recorded
one error. The failed test was:

```text
tests_tools.test_c324_locked_hash_r4.R4Tests.test_29_real_timeout_does_not_become_crash_or_success
```

Its `TemporaryDirectory` cleanup could not remove `stderr.log`:
`PermissionError: [WinError 32]` (file in use by another process).
The 211 begun modules contain 5,394 attempted tests; 1,120 tests / 28 modules were
not reached. No complete 6,514-test regression receipt was produced.
Module, regression and science processes propagated exit 1, and the runner emitted
`run_execution_valid = false`. The PowerShell error at `run_c344.ps1:19` reports
that nonzero exit; it is not the initiating error.

The `paired_pair_max_training` phase was not reached. There are no formal C344
candidate/control scores, 10-model training results, saved reconstruction, complete
final 8,183 rereads or fresh-verifier success. Numerical preflight and regression
fixture computations do not constitute the registered scientific training.

## 3. Root cause and interpretation boundary

The confirmed failure is that a timeout fixture proceeded to temporary-directory
deletion while Windows still denied delete sharing on a log file. The accepted
R4 monitor already kills and waits for its immediate child and closes its own
file handles. A missing `wait()` is therefore not a supported diagnosis.

Windows virtual-environment redirectors can create a separate interpreter process.
CPython's launcher also uses a kill-on-close job. Delayed descendant handle release
is a plausible mechanism, but the log does not identify the actual handle owner.
This recovery does not claim to prove process-tree termination or diagnose hardware.

An identical timeout/temporary-directory pattern exists in the accepted R5 test:

```text
tests_tools.test_c324_verified_session_r5.OtherTests.test_38_timeout_not_native_failure_or_pass
```

The fix covers these two historical module scopes. No scientific threshold,
candidate-selection rule, model capability or previous accepted verdict changes.

## 4. Minimal recovery contract

Revision: **C344-R1**. Only the unaccepted C344 executor, its own infrastructure
tests and its preregistration are revised. Accepted R4/R5 sources and tests,
C343 and earlier scientific sources, dispatchers and launchers retain their bytes.

While the registered R4 or R5 test module executes, C344 temporarily wraps that
module's own `b.monitor`. The wrapper calls the original monitor with unchanged
arguments and timeout. Original exceptions propagate. Non-timeout results return
unchanged. For `timed_out is True`, the wrapper performs the following cleanup barrier:

1. Open both `stdout.log` and `stderr.log` with `CreateFileW`, requesting DELETE
   access, sharing READ/WRITE/DELETE, and using OPEN_EXISTING. Do not request deletion,
   truncation, file creation or DELETE_ON_CLOSE.
2. Require both handles to be open simultaneously. If the second open fails,
   preserve its error code before closing every handle acquired by that attempt.
3. Only WinError 32 may be polled again. Use one monotonic deadline of 10 seconds
   for both files and all attempts. Other OS errors, a close failure or expiry abort.
4. Close all acquired handles, then freshly hash both logs and require equality
   with the original monitor's returned SHA256 values.
5. Return the original result object, without changing timeout, exit code,
   parent-validation status or any receipt field.

The original monitor binding is restored in `finally`. No global subprocess,
temporary-directory cleanup, Python executable or environment is replaced.
Accepted source/test identity is checked before applying the adapter.

This establishes delete readiness and unchanged log contents at the barrier.
If another actor opens a file afterwards, the original cleanup may still fail;
such a failure remains an error. This is not a blanket cleanup-error suppression,
a successful-result cache, an automatic rerun or an extension of the original
50-millisecond fixture timeout.

## 5. Early native check and complete regression

After native runtime validation and before expensive parent input hashing,
run the exact R4 timeout test three times, then the exact R5 timeout test three
times, under the same scoped adapter. These six real unittest executions must
all start and succeed, with zero failures, errors, skips, expected failures or
unexpected successes. A failed case stops immediately; it is not retried until PASS.

The six checks are additional infrastructure preflight, with no model forward,
backward or optimizer update. They do not replace or remove any full-regression test.
The execution envelope records `execution_revision = C344-R1` and the exact
`timeout_cleanup_preflight` receipt. Fresh verification validates that receipt.
No extra artifact file is introduced; the existing envelope carries the record.

After that check, retain native locks, full parent reconstruction, the original
numerical preflight, **6,514 tests / 239 fresh module processes**, scientific training,
replay, saved reconstruction, 8,183 final rereads and the fresh verifier.

Full ordered-ID SHA256 remains:
`c5d7db147680f739c62bbbc2f12be324c66ba16ea108dc04beb3071f56abaaa3`.
Parent 6,442-ID prefix remains:
`0581297af93ba5c06494f1e41627de8a2f574ee2ef62a46147225a55755ad7f5`.
Own 48 science + 24 infrastructure method IDs remain; relevant behavioral cases
are strengthened. The one inherited C204 mutable-ACTIVE exclusion is unchanged.
There is no new exclusion, skip, reduced regression or reuse of attempt-01 successes.

## 6. Scientific and protection invariants

The C344 benchmark and all 48 science tests retain their original blobs.
Manifest remains:
`a663ebb0b09671c6d277b5abec6d09604a49a194d5d61409a1a5bf5018785ad8`.

Keep seeds 344001–344005, orders 344101–344105, both mean-CE and pair-max arms,
mixed45 data, all paired initializations, input streams and splits, 2,400 updates
per model, optimizer/rates/clipping, CPU float64 / two threads, all native gates,
60 matched contrasts and four strict interior endpoints. No observed scientific
result exists to select a model, alter the cohort or relax a criterion.

Protection remains 930 sources / 8,183 inputs, with the same seven C344-owned paths.
The updated executor, infrastructure tests and preregistration are among those
protected paths. R4/R5 source and test files already belong to the inherited
inventory; exact adapter pins add checks without creating an unprotected dependency.
The six science outputs, primary, envelope and 481 regression proofs remain the
489 outputs a successor must retain.

## 7. Review and retry boundary

Before issuing a retry command, validate the changed Python code and all 72 C344
own tests, including normal and CP932-default-open author runs, actual full ID
inventory, exact source pins, ABI/error/handle-release fixtures, real subprocess
timeouts, adapter scope/restoration and early-stop ordering. Independently retrieve
and review the committed changed files through EOF. Record the tested blobs,
review HEAD and results in `docs/c344-r1-post-authoring-review.md`.

Author runtime is Linux Python 3.12.14 / Torch 2.10.0+cpu / NumPy 2.3.5.
Author checks do not establish native Windows file-sharing behavior or completion
of the formal 6,514-test run. The early six-case check is deliberately performed
again on the user's registered Windows Python 3.13.15 environment before heavy work.

Use the existing `invoke_active_v2 -> invoke_c344 -> run_c344` route on
`feat/sft-target-loss`, with the later reviewed recovery activation HEAD.
Preserve the invalid attempt. Any preflight/regression/source/artifact/native
failure stops the same C344; do not proceed to C345. A later log-publication-only
failure is repaired as transport without repeating scientific training.

## References

- [Attempt-01 log](experiment-run-logs/c344/attempt-01/latest.log)
- [Attempt-01 metadata](experiment-run-logs/c344/attempt-01/latest.json)
- [Scientific preregistration](experiment-ledger-addendum-c344-preregistration.md)
- [CPython venv launcher source](https://github.com/python/cpython/blob/3.13/PC/venvlauncher.c)
- [Microsoft CreateFileW sharing semantics](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
