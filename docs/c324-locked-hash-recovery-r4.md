# C324 recovery R4 — lock-backed hash qualification

Stage: V5-B execution recovery, not a new scientific C experiment.
Date: 2026-10-15. C325 is NOT REGISTERED. Gate F remains NOT PASSED.
C324 scientific execution 47ccd303f4382b7938db639e86aeb151e1f83af1 remains INVALID.
No scientific learning, threshold, seed, cohort, comparator or optimizer changes.

## R3 evidence and disposition

R3 diagnostic execution:4557a1fb9344596be5faf9750eae1c67e05d0b52.
R3 published log commit:9f9eb51b796665bfa35cb4834606ca37c40a0d2a.
Log SHA256:50da0a826c7a4644bce059a93d0e7598aeef482969cc27bf7c46bf53c4be0e7d.
Log size:10698 bytes. Complete remote text and terminal report were read.
No reviewer-side independent whole-log rehash is claimed; R4 rehashes the complete
local published evidence before launching its child. Immutable copies are retained
under docs/experiment-run-logs/c324/attempts/9f9eb51b796665bfa35cb4834606ca37c40a0d2a/.

R3 completed its bounded observation and publication. Its worker was terminated
at the configured180s cap: elapsed180.002s, timed_out=True, returncode1,
parent_validation_completed=False, stderr0 bytes. This is not a recurrence of
the earlier0xC0000409 native failure and is not a successful parent validation.
179 stack samples:176 real_parent_validation,3 runtime_import. Nearest repository
frame was C175.sha in171 samples;155 leaf frames were hashlib.file_digest and16
were file open. The final stack passed through C317.verify_artifacts and the
C318..C324 parent verification chain. Sampling counts are not exact call totals,
unique-file counts, unbiased time fractions, or proof of a native-crash cause.

Prior R2 found no mismatch in the C242 function it examined. Neither R2 nor R3
establishes that every cache is healthy, that hardware is faulty, or that the
original fatal interpreter error is fixed. Do not delete caches or reinstall.

## Targeted implementation, rather than another identical profiler

Candidate: process-local reuse of ONLY C175.audit.sha return values while each
input is held open by a Windows read HANDLE that excludes write/delete sharing.
C175.sha reference source blob:efd1bb246442fb4f472e33e450c16b192acfa18a.
The reference remains unchanged on disk and is explicitly checked by the guard.
The C324.load_parent call, parent hashes, recursive loader dispatch, JSON/tensor
schema checks, saved-output reconstruction and canonical prompt checks remain.
No parent validator or its result is memoized; no ancestor is declared PASS merely
because a previous run succeeded. No complete-regression result is reused.

Each cache miss acquires a read lease BEFORE reading bytes, uses streaming SHA256,
and compares its digest to the original C175.sha under that lease. Every hit
checks held-handle identity plus a newly opened path identity. Leases remain open
until the entire candidate validation and final uncached-reference recheck finish.
All unique files are reread by the original SHA function at the end. Any mismatch,
lock failure, unexpected thread, missing path, changed identity, short read or
4096-file bound violation stops; no unlocked/evicting fallback is permitted.

This is not a timestamp-only cache. It uses native non-inheritable HANDLEs rather
than retaining thousands of CRT descriptors. The data are not copied into RAM:
only per-file handles, identities, digests and counters are retained. Leases close
on exceptions; process termination also ends this process's open-handle lifetime.
The dictionary is discarded between processes/runs; no persistent PASS cache.
Reparse-point/directory handles are rejected. Runtime use is Windows-only, with
no POSIX advisory-lock substitute. Arbitrary hostile kernel/filesystem behavior
is outside this operational integrity model.

Native semantics reference:
https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew
https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle
https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfile
CreateFile sharing restrictions remain until handles close. FILE_SHARE_READ permits
readers but not conflicting write/delete access; preexisting incompatible writers
or writable mappings cause opening to fail. No permission changes are made.

## Exact operational scope

One child process;300s controller wall-time cap including imports, native probe,
parent validation and final reference rereads.10s heartbeat; no automatic retry.
At startup create ONLY a small new lock-probe file inside the new local run folder.
Verify actual Win32 read compatibility, denial of WRITE/DELETE access while the
lease is held, and release afterward. The probe requests rights without modifying
or deleting any existing data. An unsuccessful native probe stops before archives.
Then verify the same CPython3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5 environment.

Call the unchanged C324.load_parent ONCE, using all50 registered ordered paths.
Use the original no_neural guard plus explicit model-forward, optimizer and child
science-entry prohibitions. Parent tensor archives may be loaded for validation;
no model forward, optimizer update, full regression or scientific run is started.
No -O flag, environment-version change, cache deletion or data overwrite.

Capture hash_calls, cache_hits, unique_files, streaming bytes, reference bytes,
logical-reference bytes and final recheck count. These are adapter-scoped logical
payload counts, not physical disk I/O. On interrupted reads, reference_bytes is a
requested-size accounting bound, not a completed-byte count. Report completion
and exceptions separately; no fabricated wall-time speedup or extrapolated share.
A full original-path baseline is NOT rerun for hours just to claim a ratio.

## Qualification boundary and transport

Success requires actual native-lock probe, complete parent validator return,
canonical192/96 data, restored original hash function, every unique uncached
reference recheck, valid receipt, zero child exit and no timeout. A timeout is
incomplete qualification; fatal exit is retained as such. diagnostic_completed
only means the controller collected the outcome, never scientific C324 PASS.

Files are local-only below a fresh runs/c324-locked-hash-r4-* directory:
stdout/stderr, lock-probe.bin, hash-inventory.json, worker-result.json if completed,
and diagnostic-report.json. Only the console log is published by the standard
C324 transport. Role is C324-R4-LOCKED-HASH-QUALIFICATION. End action always
STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY. No C325 and no automatic full C324 run.

## Authoring and activation boundary

37 tests cover streaming/reference parity, raw Win32 ABI and access flags through
an explicit emulator, cache hits, mutation, same-size/mtime-restored corruption,
lock errors, failed misses, bounds, cross-session invalidation, cleanup, parent
call/exception passthrough, source guards, complete R3 evidence hash,50 paths,
real subprocess failure/timeout, receipt and launcher contracts.
Emulated Win32 tests and synthetic parents are NOT native Windows qualification.
The actual native lock test runs first on the user's environment. Full5357 remains
required for a later scientific run. Scientific sources/tests/runner are unchanged.

Activation requires committed remote-file reread, byte identity, tests and a
separate post-authoring review record. This source contract alone is not an
execution authorization. The authoritative handoff selects LOCKED_HASH_R4 only
after that review. Do not repeat old R2/R3 commands.
