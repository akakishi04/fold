# C336 R1 -- exact registered lock capacity

Date: 2026-10-20 Japan time.
Stage: V5-B-SAVED-QUERY-ORDER-PATTERNS.
Verdict: INVALID EXECUTION / RETRY SAME C336.
C335 remains ACCEPTED VALID NEGATIVE; Gate F NOT PASSED; C337 NOT REGISTERED.
This is an execution repair, not a new hypothesis, result or scientific retry selection.

## Attempt 01 identity and observed failure

Scientific execution HEAD: c0efb27bbabe969d5f90667437deadb1d9a39dec.
Publication: de6d6bb1d43b69d26f0463426fbf56229871d087; sole parent equals execution.
Metadata reports 7699 original Windows bytes and SHA256:
f7436128435da8e2448860f3898bbbc4ca64a2cf549c34d6383044a41b2af7de.
Log blob: 0a993e3ff2228f527e2f537b76d50502c6e807ba.
Metadata blob: 300db5a3e39d746dc0b0dc0ac62cc861f7487dca.
Exact Git-blob copies: docs/experiment-run-logs/c336/attempt-01/latest.log and latest.json.
Original latest files remain unchanged. Do not erase the local failed run directory.

The native read/write/delete-sharing probe passed. The science worker stopped in
snapshot -> parent_test_files -> C324 LockedHashes.sha while adding mandatory C335
module evidence. Exception: locked-file bound exceeded; no eviction fallback.
Science exit1; run_execution_valid=false. C336 full regression, response-pattern
analysis, final rereads and fresh verification were NOT reached. Parent validation
was in progress, not completed. The console's run_c336.ps1:19 reports this earlier
Python exception; it is not the first failure site. No native access violation was
observed in this attempt. Log publication succeeded independently of execution.

## Confirmed implementation error

Accepted tools/c324_locked_hash_r4.py defines MAX_FILES=4096 and exposes an explicit
max_files constructor parameter. C336 scientific_worker omitted that argument.
C335's registered3893 inputs fit the default. C336 requires4360=3893 inherited+
461 immediate-parent files+6 own files, exceeding the default by264.
The failing branch checks len(entries)<max_files before acquiring the next lease.
This is the executor's configured bound, not evidence of RAM exhaustion, a Windows
handle limit, corrupt saved models or insufficient disk space.

The previous author test used synthetic ancestor-map entries and a permissive
cache collaborator; it did not exercise the complete input union through the real
cache. Consequently the previous review missed this resource-capacity mismatch.

## Minimal repair and invariant boundary

Only unaccepted C336 executor and its own test file change. Scientific worker passes
max_files=s.INPUT_COUNT (4360) when constructing the unchanged accepted LockedHashes.
It prints locked_input_capacity with max_files and protected_inputs before snapshot.
Do not change the inherited MAX_FILES, class methods, lease implementation or source
pins. No unbounded cache, eviction, unlocked fallback, skipped evidence or runtime
retry. Exactly4360 distinct protected entries can be retained; a4361st distinct
entry is rejected before a new lease is acquired. Reuse does not consume another slot.
This capacity bounds cached protected-file leases, not every transient process handle.

Keep all existing initial independent hashes, held-lease checks, complete parent proof
reconstruction, 4360 final uncached reference rereads, output binding and fresh verifier.
The scientific benchmark and its manifest remain byte-identical:
benchmark blob78e33df0faed7cddcc888d4c068f8026327d99e8;
manifest e6f992e680bc4b80284dbc04366566f737fb1bfd3f55fb0ac10d76d90ebd76af.
No modification to tools/c324_locked_hash_r4.py (blob6459b1f6e4051fbfc54db2894f7abe3a7521df3a),
accepted C335 or earlier files, launcher, runner, active dispatcher or preregistration.
Operational repair is documented here; scientific schemas, own-file inventory and
manifest do not change. The exact execution HEAD/source blobs identify the revision.

Same32 own test IDs,6090 full tests/226 modules,877 sources/4360 inputs. All10C335
states,12960 quads/6480 paired quads/51840 normal answers/720 strata stay fixed.
No new scientific model forward,training,gradient,optimizer update or checkpoint.
C335 remains negative; any diagnostic distribution remains admissible.

## Strengthened author checks

Extend test22 without dropping its original proof/tamper checks. Materialize all3893
synthetic ancestor inputs and the461 parent outputs plus6 own sources. Execute the
production C336 snapshot and parent-proof path with the REAL accepted LockedHashes.
Only the lease object and historical proof/semantic collaborators are explicit
software fixtures; no native Windows sharing or genuine C335 artifacts are claimed.
Reproduce failure with the default4096 cache, then complete the same snapshot at4360.
Verify every input receives one independent initial and one final reference hash,
all leases remain held until exit, cache hits do not acquire new leases, the4361st
file fails without eviction, and cleanup succeeds after success or exception.
An equal-size byte mutation must still fail the final uncached reference recheck.

Strengthen test29's worker collaborator to require an explicit integer max_files
identical to the registered input count; it no longer ignores constructor options.
Keep the existing worker/fresh-verifier ordering and diagnostic-flag tamper checks.
Restoring the default or a larger arbitrary capacity must be detected by this test.
The ordinary32-test suite passed before source publication. Committed-byte reread,
post-reread normal/CP932 runs, mutation controls and independent author review must
still complete before a retry command is issued. No full6090 native success is
claimed by the local author suite.

## Invocation and stop

Existing active_v2 -> invoke_c336 -> run_c336 -> c336_execution route is unchanged.
Expect locked_input_capacity={max_files:4360,protected_inputs:4360}, then complete
parent validation,6090 module-isolated tests,unchanged diagnosis,all final rereads
and fresh verification. Require persisted_query_order_patterns PASS,
execution_envelope_verified and run_execution_valid=true,then log publication.
Any technical failure stays SAME C336. Never bypass RESULT_ALREADY_PUBLISHED with
a publication HEAD; never rerun C335 training. No C337, automatic retry, package
installation, paid service, CI, accepted-source edit or artifact deletion.
