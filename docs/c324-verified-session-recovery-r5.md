# C324 recovery R5 — verified-session qualification

Stage: V5-B execution recovery. Date: 2026-10-15.
C324 scientific attempt47ccd303f4382b7938db639e86aeb151e1f83af1 remains INVALID.
C325 NOT REGISTERED; Gate F NOT PASSED. No change to model, seed, data, optimizer,
learning budget, threshold, cohort, comparator or scientific result interpretation.

## R4 disposition and actual evidence

Diagnostic execution9b8ef0895899d12fa17b244d766cfa5f3c431dc6.
Published loga443d7b3b9db6202cf4edcdc98ecedab930aea72.
Metadata7403bytes;SHA256e83f4878f25a4555c3fee4aef2281c4b37f8d423de761f3ff50a5b2f73eb964a.
Complete remote console text and final report read. No independent reviewer-side
whole-log rehash is claimed. R5 rehashes the local published R4 log before its child.
Exact R4 log blobs archived under attempts/a443d7b3b9db6202cf4edcdc98ecedab930aea72/.

Controller completed and published; worker reached300s cap (300.009s), exit1,
timed_out=True, parent_validation_completed=False, stderr0bytes. This is bounded
incomplete qualification, not another observed0xC0000409 fatal and not parent PASS.
The actual Windows native lock probe passed read compatibility, denial of WRITE
and DELETE access, and release. No final reference rereads were reached.

LAST REPORTED hash progress at283.824s, not an invented terminal counter:
hash_calls206916;cache_hits205434;unique_files1482;stream_bytes12445062684;
reference_bytes12445062684;logical_reference_bytes878894660237;
final_reference_rechecks0. Logical requested bytes are not physical disk traffic.
Hash reuse operated but full validation and its final integrity check did not finish.
No controlled runtime speedup or native-crash repair is established.

## Source-level reason for the next change

The C317..C323 load_parent functions call an immediate parent's verify_artifacts,
and several subsequently call that parent's load_parent again for data. The
verifier itself calls load_parent. R4 reduced repeated hashing but did not reuse
completed semantic reconstructions, archive analyses or repeated verifier results.

This R5 contract explicitly introduces a NEW qualification scope: reuse of the
complete return values of EXACTLY C316..C322.verify_artifacts, within one isolated
read-locked validation session. R4's no-validator-cache rule remains true for R4;
R5 does not retrospectively change R4 or silently authorize a production cache.
C323.verify_artifacts and C324.load_parent remain original. All load_parent
functions remain original. The source files of all seven verifiers remain unchanged.

The seven source files and full verify_artifacts bodies were read at the R4 log
commit. They return (summary, measurements), not a model or open archive. Each body
validates its summary/identity, hashes protected inputs and artifacts, invokes its
parent loader, reconstructs the saved measurements from its tensor archive, and
compares persisted JSON and summary. Neither an old recorded PASS nor header-only
validation replaces that first body execution.

## Snapshot and reuse contract

1. Verify the accepted C323 summary against C324.PARENT_SHA and its existing
   validate_parent contract. Freeze the complete input_sha256 inventory, all50
   ordered summaries and every C323 output. The digest map comes from a pinned
   summary, not untrusted paths selected by a cache hit. Merge only identical
   path/hash aliases. Every registered source pin must have protected raw bytes.
2. Compare inherited source blobs using one exact NUL-delimited Git tree inventory.
   Check the fixed blobs of the seven verifier modules and the unchanged R4 helper.
   Also lease the operational R4/R5 helpers and current C324 implementation.
3. R4 native Windows read leases are acquired before verifier reuse and held through
   all reconstruction and final reference rereads. No timestamp-only validity,
   unlocked fallback, persistent cache, external training or filesystem mutation.
   An undeclared hash input is rejected rather than silently expanding the snapshot.
4. Cache keys include verifier name, operational HEAD/source blob, output directory,
   ordered parent paths and expected execution HEAD. Runtime/RNG context must match.
   Before each call, check all held/current path identities and every selected
   module binding/manifest seal. Changed function code, source, arguments or data
   cannot inherit an earlier result. Reentrant identical calls and extra threads fail.
5. On a miss, execute the unmodified verifier body; nested selected verifiers obey
   the same rule. A failed call is never stored. Successful returns must be a
   metadata tuple; retain a separate deep copy and type-aware fingerprint. Every
   hit returns a new deep copy; parent/caller mutation cannot pollute another use.
   No model weights, evaluation tensors or pickle archives are retained in this
   result cache. Metadata is bounded to16entries and64MiB serialized representation
   (not a claim that total process RSS is64MiB).
6. Restore all seven original functions and original SHA, then finish the original
   C324 parent-result/canonical192/96-row checks. Require each selected verifier
   body to have executed successfully exactly once, with actual reuse observed.
   Independently reread EVERY locked input with the original SHA before release.
   Discard all cache entries on success or error. No reuse across processes/runs.

The equivalence argument is conditional on fixed input bytes/source/runtime and
the deterministic read-only verifier contracts above. It is not a proof against
hostile kernel/filesystem behavior or all possible native-memory faults. A complete
native run remains required. Induction starts at the unmodified older validators:
first execution is real; repeat requests reuse only the exact validated metadata.

## Operational workload and boundaries

One child process;600s controller cap includes imports, lock probe, initial complete
snapshot, one C324.load_parent call and final uncached reference rereads.10s heartbeat.
This cap is not a promised total duration or speedup. No full reference replay is
run for hours merely to claim a timing ratio. No automatic second attempt.

Exact Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5 and CPU2threads/deterministic
configuration remain. Native Windows lock probe runs first. Original no_neural,
explicit model-forward/optimizer/scientific-entry prohibitions remain. Full5357
regression and scientific learning do NOT run in R5; they remain necessary for a
later separately authorized full scientific recovery. No C325 is consumed by R5.

Keep per-verifier requests/executions/reuses/failures, metadata size, frozen input
inventory, hash progress, final reference count, source identities and canonical
outputs. Counter scopes remain explicit. Controller diagnostic_completed is only
an outcome-collection flag. Qualification needs exit0, no timeout, full parent
return, exact checks, all7 first executions and every final reference reread.
Regardless of outcome: STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY.

## Authoring and review requirements

48 software tests exercise exact-key reuse, wrong source/head/order/directory,
first/hit caller mutation, stored-result corruption, runtime/code drift, failure
non-caching, bounds, threading/lifetime/reentry, metadata types, initial/late input
corruption, leases, real Git tree parsing, RNG observation, real subprocess errors
and timeout, full R4 evidence hash, complete snapshot construction and routing.
A seven-level synthetic graph gives identical reference/candidate values with127
versus7 verifier body calls. This is a software fixture, not production speedup.

No actual Windows or the user's local50-parent archives exist in the authoring
environment. Emulated leases are explicitly software fixtures; no production
switch selects them. R4 native success does not qualify the new R5 semantic cache.
Post-authoring review must reread the committed files and compare Git blobs to
retested local bytes before handoff selects VERIFIED_SESSION_R5. No change to
accepted scientific source/tests, protected dispatchers or historical verdicts.
