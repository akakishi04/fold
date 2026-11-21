# C324 recovery R4 — post-authoring review

post_authoring_review = PASS
Review target HEAD: e542ee01c2af85abff4a44952d36ba34659230c4.
Review date: 2026-10-15.
Base: 9f9eb51b796665bfa35cb4834606ca37c40a0d2a (published R3 diagnostic).
Scope: bounded lock-backed hash qualification software readiness only.
NOT a native Windows qualification, measured production speedup, native-crash fix,
full 5357-test regression success, scientific C324 verdict or authorization for C325.

## Committed remote-byte review

All four executable/test files were fetched again at the immutable target HEAD
and reread after committing. Large Python files were retrieved in consecutive
ranges through their entry points. Their returned Git blobs match independently
computed local raw-byte Git blobs. The complete R4 operational contract was also
reread. No executable source was changed during this review.

| Path | Verified Git blob | Bytes |
|---|---|---:|
| tools/c324_locked_hash_r4.py | 6459b1f6e4051fbfc54db2894f7abe3a7521df3a | 21850 |
| tests_tools/test_c324_locked_hash_r4.py | f6d52c5464b967e3a48eefe12f5c83ea65f9f3a8 | 20232 |
| tools/invoke_c324_locked_hash_r4.ps1 | de55adde3f29f271e6af1bb04137252c040c8168 | 2868 |
| tools/invoke_c324.ps1 | cb1bf5992c9b718dfcbb012aa01d0a996d7f6b8d | 9160 |

All four files decode as UTF-8 without literal NUL. Both Python files compile.
The symtable/free-global audit found zero unbound names in both Python files.
Source-string tests were checked against the actual named function bodies.
The existing C324 launcher differs from its prior blob
0261088b3cf340b3cc8f41959197647586ff9b73 by exactly one recovery-action map entry.
All 50 ordered parent paths, normal scientific body and publication logic remain.

## Tests actually executed after remote matching

Linux / Python 3.13.5; isolated authoring workspace.
Command: python -m unittest tests_tools.test_c324_locked_hash_r4 -v

37 tests ran: failures 0, errors 0, elapsed 2.320 seconds.
The same 37 tests with default text-file opens explicitly emulated as CP932:
failures 0, errors 0, elapsed 2.355 seconds.

Real operations include temporary-file hashing, streaming byte parity, same-size
changed-content cases, restored timestamp corruption caught by the final reference,
cache lifetime/bounds/thread guards, cleanup, subprocess nonzero exit, process
termination at a short test timeout, receipt serialization and launcher contracts.
The parent-loader integration uses an explicitly synthetic parent and tests call
count, reference restoration and unchanged propagation of parent rejection.
The Win32 adapter uses an explicitly injected ABI/share-access emulator; it is
NOT a native Windows locking test. The production executable has no CLI option
for this emulator and fails without native Windows support.

No local PowerShell executable was available. No PowerShell AST execution is
claimed. The user command parses the active dispatcher; the dispatcher parses
C324's launcher; its recovery branch parses the selected R4 launcher before use.
The actual native lock probe executes FIRST in the user's worker, before parent
archives are read. A failed probe is retained and does not permit an unlocked run.

## Intervention and integrity review

Only C175.audit.sha is temporarily substituted. The accepted C175 file remains
unchanged and its Git blob is pinned by the diagnostic guard. Every parent loader,
semantic validation, artifact hash comparison and canonical data check still runs.
No parent verifier result is cached, no past success becomes a new PASS, and no
historical test or scientific source is modified.

Native API signatures and share-mode behavior were checked against Microsoft
CreateFileW, GetFileInformationByHandle and ReadFile documentation. Every cache
miss holds an OPEN_EXISTING read HANDLE without write/delete sharing before reading.
The candidate digest is compared to the original SHA function under that lease.
Each hit checks the held identity and the current path's independently opened
identity. All unique entries receive a final uncached original-function reread
before the leases are closed. Cached state is process-local and never persisted.
Locks/errors/bounds/identity drift cause a stop, not an unlocked fallback.
This operational model does not claim protection against arbitrary hostile
kernel/filesystem behavior. It is not a general-purpose security sandbox.

C324.load_parent is called exactly once with all 50 original ordered summaries.
The actual parent validator must return, canonical data counts must match, and
all final reference rechecks must complete before parent_validation_completed
can become true. Model forwards, optimizer construction and scientific entry
points remain blocked. The scientific seed/threshold/workload contract is untouched.

## Controller, evidence and activation boundary

R4 checks the complete R3 console bytes against its published SHA256 and reads
its report before launching one worker. The worker's 300-second cap covers imports,
lock qualification, parent validation and final reference rereads; it is not a
promise for total launcher/log-publication duration. Ten-second heartbeats are
rate limited so the R3 end-of-timeout repeated-heartbeat behavior is not inherited.
Nonzero exits and timeouts remain distinguishable; a zero exit without the full
worker receipt is not a successful qualification. No retry loop or auto-science.

Adapter counters describe logical payload reads, not physical disk I/O or unbiased
wall-time shares. Reference-byte counts during interrupted reads are requested-size
bounds. No full original-path baseline speed ratio has been measured or claimed.
A successful R4 qualification still does not prove that the original CPython fatal
error has been fixed. Scientific C324 remains INVALID ATTEMPT RECOVERY.

The activation commit adds this review and changes the authoritative handoff only.
Use that final activation HEAD, not the source-only review target, in the user's
launcher command. The sole authorized next action is LOCKED_HASH_R4, then STOP.
