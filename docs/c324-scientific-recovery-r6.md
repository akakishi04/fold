# C324 R6 - scientific retry after verified-session qualification

Stage: V5-B execution recovery. Authoring date: 2026-10-16.
This is the SAME C324, not C325. Gate F remains NOT PASSED.
The old scientific attempt at47ccd303f4382b7938db639e86aeb151e1f83af1 remains INVALID.
R6 authorizes a new attempt only after its committed-source review is PASS.

## R5 disposition

R5 diagnostic execution:1beb6d60f3dd0f7c72f41c9355c96827b8da4e82.
R5 publication:f7a909f2e1a0b4bd5d03c0a54bcb63519b022b19.
Log SHA256:2f89e566132f0ade3660dc7c2aafb6a4946ffaa3d441341af0d39671cd663558.
Log15940bytes. Remote progress and complete terminal report were read; publication
parent equals execution HEAD. No independent reviewer full-log rehash is claimed.
The R6 controller rehashes the complete local published log before starting.
Exact original log blobs are preserved under attempts/f7a909f2e1a0b4bd5d03c0a54bcb63519b022b19/.

R5 QUALIFICATION PASSED: child244.561seconds, exit0, no timeout, stderr0.
All7 C316..C322 verifier bodies completed once,9 exact repeat requests reused.
1486 distinct files were locked and all1486 reread by the uncached reference.
Hash61762requests =1486first reads +60276hits; final reference rechecks1486.
Retained metadata24083208bytes. Parent including final rereads173.9249438seconds
excludes earlier imports/snapshot acquisition; do not equate it with whole-worker
244.561seconds. Canonical data and original prompts match C324's pinned digests.
Interior prompts:e7f9a53e162f5f0156261e33c0bac7875ee592fbd2bdb2d27faac4f3d27f5e8b.
No new model forward or training. This qualifies the operational mechanism on the
actual archives; it is not a scientific C324 PASS or proof of the crash's cause.

## Scientific conditions stay fixed

The original C324 source blob remains2fc9e31c7037313a3fadb126af9b153608c0ac6e.
Original manifest:b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
No edits to fold_lm,fold_reasoning,tests_lm,tools/run_c324.ps1 or old results.
Same original/interior4 arms, native mean_last, length4 TRAIN-template intervention,
seeds324001..324005, orders324101..324105, CPUfloat64,2threads,14256parameters,
64slots,1200updates/model,48rows/update, same optimizer and gates.
Child work12000updates,576000training rows,15420forward calls,904320row presentations,
61680core forwards,10checkpoint reloads. Software probes and validation stay separate.
A finite scientific FAIL is retained and can be valid negative evidence; it is NOT
an invitation to change a seed, threshold or learning budget and train again.

## Operational integration

R6 first reads the complete pinned C323 input inventory and50 ordered summaries.
It reuses the unchanged R4 native Windows read leases and the unchanged R5 verified
session for C316..C322. Each original verifier body executes once; exact repeat
requests use isolated, fingerprinted metadata. Full first-time semantic checks are
not replaced by old recorded verdicts. R4/R5 native/reference source blobs are fixed.

The completed C324.load_parent return consists of4 dictionaries: parent summary,
canonical logical data, original prompts, interior prompts. R6 retains a deep copy
of this parsed data while all inputs remain read-locked. It checks that the first
real parent load preserves Python/NumPy/PyTorch RNG and runtime context. Model calls
and optimizer construction are prohibited during that original reconstruction.
All seven verifier substitutions and the SHA substitution are then restored.

Subsequent C324 runtime_preflight, run and verify_artifacts receive isolated copies
of exactly that parsed data, with ordered path checks, all lease/path identities,
and a type-aware fingerprint checked every time. This is explicit new R6 scope:
parsed input reuse across phases of ONE process, not cached model outputs or reuse
of a historical PASS. Parsed JSON is independent of subsequent training RNG/grad
state; reading it must not consume or restore RNG. On exception, release leases and
clear the data; no across-run persistence and no unlocked fallback.

Git source verification is batched without changing its answers: one ls-tree plus
one cat-file --batch inventory supplies exact HEAD:path and known blob replies.
Every canonical blob has its Git object hash checked; raw working bytes must be
exact canonical LF bytes or their complete CRLF expansion. Other Git commands,
including live HEAD/branch/status guards, still invoke Git. No Git guard is cached.

Within the locked worker:
1. Build the full protected snapshot and run the actual optimized parent validator.
2. Run unchanged C324 native TRAIN/schedule/gradient preflight.
3. Run the ENTIRE regression in a SEPARATE unmodified Python process; no validation
   substitutions leak into tests. Preserve original ordered5357tests and its sole
   inherited C204 exclusion. Append R4(37),R5(48),R6(48):5490selected,213modules,
   5491before the single historical exclusion. No new skipped/excluded tests.
4. Only after full success, run unchanged C324.run:10new models, evaluation, saved
   checkpoints and10exact replay checks. No partial cohort or seed selection.
5. Run unchanged C324.verify_artifacts: reread saved checkpoints/evaluations and
   reconstruct ALL saved metrics/JSON. It uses the still-locked canonical parents,
   not cached child results. This verification is in the scientific worker.
6. Restore the substitutions, independently reread ALL1501locked files with the
   original SHA, release leases, and persist the additional execution envelope.
7. A fresh process checks the envelope, current source tree, every input byte,
   scientific summary contract and every saved output's hash and size. This final
   process does NOT rerun ancestor semantic analysis or claim to do so.

## Mandatory composite evidence / deciding-path protection

The original C324 summary schema and its792source/1491input contract stay intact.
R6 does NOT pretend that these792pins cover the newly added execution machinery.
The mandatory companion execution-envelope.json contains the FULL UNION:

-802 source pins =792 primary +10 supplemental files;
-1501 protected input files =1491 primary +10 supplemental files;
-5490-test complete result, seven real verifier completions and reuse counts;
-primary summary SHA256, original manifest and scientific work, saved semantic
 reconstruction completion, final1501uncached rereads, parsed-data read count;
-R5 evidence identity, hash/Git counters and separately scoped timings.

Supplemental10: R4/R5/R6Python helpers; R4/R5/R6test modules; R4/R5/R6launchers;
this R6 contract. The main invoke_c324 launcher is already among the primary792.
All direct runtime code and the extra regression inputs are pinned and read-locked.
The fresh-process verifier checks primary maps are exact subsets of the envelope,
not just cardinalities. Both summary AND envelope are mandatory for acceptance.
A future C325 must validate and inherit the composite802-pin protection; consuming
only the old792-pin summary is insufficient and must NOT be registered as complete.
No accepted result or prior contract is rewritten to hide this additive protection.

Output remains local-only under runs/c324-scientific-r6-<id>/, with science/summary.json,
science/8registered outputs, execution-envelope.json, snapshot-inputs.json,
regression-result.json and process logs. Only console text is published as C324.
No model/tensor/data artifacts enter Git. The envelope hash is printed in the log.

## Workload, logging and stops

This is now a full scientific run, not a600second diagnostic. No R5 diagnostic cap
is applied to training or full regression. The controller streams actual child
output and emits10second heartbeats. No total duration or controlled speedup is
promised. Timings for snapshot construction and whole worker are separated.
C324's original runtime.elapsed_seconds now covers its run phase with reused input
preparation; it is not directly comparable to old multi-hour parent-inclusive time.
Peak process RSS still includes this worker's earlier parent reconstruction.

Route:active_v2 ->invoke_c324 ->invoke_c324_scientific_r6 ->R6 controller ->science
worker ->separate regression process ->training/postcheck ->fresh envelope check.
Authoritative Python3.13.15/PyTorch2.10.0+cu130/NumPy2.3.5 remain fixed.
No packages reinstalled, cache deleted, checkpoints reused for fitting, or CI added.

run_execution_valid=true requires all of the above. Native fatal, exception,
nonfinite, incomplete tests, schema/source/input/replay/envelope failure retains
an INVALID attempt and stops SAME C324. No automatic repeat and no C325.
Scientific status FAIL with complete valid execution is not a process failure.
If only log publication fails, repair transport without rerunning training.

## Authoring gate

48 new tests cover exact Git batch parsing/parity and real Git, source LF/CRLF,
source corruption, parsed-data copies/mutation/ordered requests/lifetime/RNG,
full R5 proof identity/completion, exact additive suite inventories, failed-suite
rejection, subprocess error preservation, launcher guards, and execution ordering.
Synthetic production-worker integration executes the real R6 control function with
explicit fake scientific/model/lease dependencies and checks preflight ->regression
->training ->saved semantic verification ->final reread. It also checks a failed
regression cannot reach fitting. These tests are NOT native Windows or FOLD fitting.

Before activation, reread committed remote source/test/launcher/contract bytes,
recheck blob identity and execute new tests again. Native PowerShell AST checks
remain mandatory in the user's dispatcher ->launcher chain. Do not claim native
Windows/full5490/scientific PASS from author-side fixtures.
