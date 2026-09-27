# C268 execution recovery — protected dispatcher restoration

## Verdict and evidence

C268 INVALID EXECUTION / RETRY SAME C268. C269 NOT REGISTERED; Gate F NOT PASSED.
The published attempt failed during C268.precheck -> C267.verify_artifacts -> input_sha256 validation,
with ValueError: postcheck input. No C268 own tests, focused regression or scientific training began.
Do not interpret this as a capability failure, change training settings or move to C269.

Execution HEAD:8c464589b7f9e339b1a8d195b2d73d35c1279e39.
Invalid log publication:ddcb69e11a812cc3d59ebcf66c223cfd5c347249.
Log:docs/experiment-run-logs/c268/latest.log at that immutable commit.
Publisher log SHA256:60464755e769f80de86a04d474abf5a6d23b71ad2d72b33f15665150b2683abf;1619 bytes.
The current latest files are preserved by this recovery; future attempts may replace latest while
this commit retains the invalid evidence. The earlier user-reported utf8NoBOM publication exception
was a separate host-compatibility symptom. The now-published traceback is not a Python quote error.

## Root cause and responsibility

The assistant's earlier operational fix fece51c05c2b38ffa2e96ea601fc4b8a127305b8 modified
 tools/invoke_active.ps1 in place, despite C267 storing that file in BOTH source_blobs and input_sha256.
C267 requires Git blob86b5606a5b212b12f416abedac0923da634f88e3 and Windows CRLF byte SHA256
57a0f1ffa3a9370b5261ec5bf1e9eb3d778dc84f19f35c51e21174f61735a95b.
The operational patch had blob ea2e3d59cc72f0fa799f61d632f864c366099a89 instead.
Thus the child's unchanged parent verifier correctly rejected the changed file. A clean Git working
tree does not mean the working files still match an earlier experiment's pinned bytes.
The prior review called it control-plane code but failed to check the actual inherited pin mapping.
Do not blame the user or bypass the hash check. The published log contains no other mismatch paths;
additional local mismatches are not ruled out without the authoritative retry precheck.

## Minimal repair — no pin exemptions

Restore tools/invoke_active.ps1 by reusing the exact accepted Git blob, not by editing its content.
Keep its historical Windows CRLF representation on checkout. Leave C267's summary, source mapping,
expected SHA256, verifier, numerical code, datasets and checkpoints untouched.
Move operational enhancements to the NEW tools/invoke_active_v2.ps1 entry. It performs:
- PowerShell Core >=7.3 guard before scientific logging and Standard native argument passing;
- branch, tracked-tree, exact ExpectedHead and unique formal ACTIVE checks;
- published-result notice only for matching metadata and matching log hash/size;
- genuine stale-HEAD fallback without substituting current HEAD;
- explicit legacy Git-blob and raw Windows-byte checks, with expected/actual values on failure;
- self and selected-launcher ParseFile checks; the launcher retains the runner parser.
The C268 launcher also rejects old PowerShell before starting logging/publication.
Do not rewrite any file or hash automatically when a preflight fails.

This is an explicit operational override of the old generic invocation instruction: use
 tools/invoke_active_v2.ps1 through the installed C:\Program Files\PowerShell\7\pwsh.exe.
The original invoke_active.ps1 is now a preserved historical dependency, NOT a mutable place to
add future safeguards. Later operational revisions must use new versioned paths and corresponding
immutable tests. RESULT_ALREADY_PUBLISHED is evidence availability, never acceptance or PASS.

C268 test24 now verifies the exact historical dispatcher and the new entry's fixed content SHA256,
then retains the old guard/metadata/parser assertions on the new entry. Its new normalized UTF-8
content SHA256 is68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10.
This control-plane file is additionally pinned through that C268-owned test; it is not a new
scientific Python dependency or an exemption from inherited input validation.
Tests01..23, benchmark, runner, manifest and scientific preregistration are unchanged. The existing
OWN6 registration still protects the changed C268 test/launcher. Counts remain454 source pins,
774 protected inputs,24 own tests,3597 focused tests. No historical test exclusion is added.
Margin2,coefficient0.1,800 updates,10 models,seeds268001..268005,CE comparator,data split and all gates
remain fixed. C267 remains ACCEPTED VALID NEGATIVE.

## Review boundary

This recovery must receive committed-byte readback and review before a new command is issued.
The local review executes the changed test24 body isolated from its unrelated neural setUpClass,
checks the other23 test bodies are unchanged, and independently hashes the restored dispatcher.
Windows CRLF hash is reproduced from the accepted Git blob; it is NOT read from the user's PC.
No PowerShell executable or complete repository/runtime artifacts are available to the reviewer.
Do not claim PowerShell execution, full own24, full3597 regression or user-parent precheck PASS.
Those remain mandatory in the user's runtime before any training. Record the actual review target
and result in the main handoff. Recovery does not register a new C number.

## Stop

Use only the final reviewed recovery HEAD. If the legacy raw-byte guard fails, stop and report its
expected/actual values; do not normalize all files or change Git settings blindly. Any remaining
parent-input mismatch requires identification, not an allowlist. Keep C268 until a valid run exists.
