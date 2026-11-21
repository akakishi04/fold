# C342 independent post-authoring review

Date: 2026-11-02 Japan time.
post_authoring_review = PASS
Reviewed source/preregistration HEAD: eb9ddb8388df4e2321b6b2e88769a827dd6cd09b.
Tree: e79e63ffc78b812dc264d58b36573126b9fafc1e.
Sole parent / separate C341 acceptance: d8ab608b482d877a3927ef48b0f03a4212451aa1.
This is authoring review, not native Windows/full6378/scientific PASS. Execution
uses the subsequent documentation-only activation commit, not this source HEAD.

## Independent committed-byte review

The reviewer is distinct from both implementation authors. After all seven files
were published, the reviewer fetched each at the exact source HEAD, read through
EOF, and compared remote blobs, committed Git tree and locally tested bytes.
No blocker or source correction remained. Root separately fetched the commit and
verified complete tree equality with the author-tested content before final checks.
The source diff is exactly seven additions; accepted sources/tests/contracts/logs,
read-lease implementation and dispatchers are unchanged. No pending seal remains.

|File|Git blob at reviewed HEAD|UTF-8 bytes|
|---|---|---:|
|fold_lm/v05_benchmarks/model_c342_mixed_length45_training.py|7a3d1c3d2aca1cb3b632a2ef490fff5c76028289|34995|
|tools/c342_execution.py|780274ffd0236d0a24147cfb7a9b7015ee4eb0a5|27718|
|tests_lm/test_v05_c342_mixed_length45_training.py|e01c7afa1a0070fe6182445b2875b267df2e6ce4|30576|
|tests_lm/test_v05_c342_execution.py|1fa69203a95a6e90515a607e47800831272c32a7|29247|
|tools/run_c342.ps1|c6c424b0a422d027a888963c120ae79bd92cec4b|966|
|tools/invoke_c342.ps1|28449b43ca47eb8cb0b79802f41820552b2b3451|3150|
|docs/experiment-ledger-addendum-c342-preregistration.md|4514912a9d92fd26ab6fe7ae950f596ce3ae64f9|18012|

## Executed checks after publication

- Combined 64 own tests: PASS, 65.235 seconds; failures/errors/skips/expected-failures/
  unexpected-successes all zero.
- CP932 default-text-open emulation: 64/64 PASS, 65.540 seconds, all exception
  counters zero. builtins.open and io.open use CP932 only when text encoding is
  unspecified or locale; explicit encodings and binary mode are unchanged.
- Both test runs use fresh PYTHONPYCACHEPREFIX paths and -B. The reports bind the
  exact eb9ddb8388df4e2321b6b2e88769a827dd6cd09b HEAD.
- All seven files decode as UTF-8 and contain no NUL. Four Python files exactly
  match git-show bytes and compile/import. Pyflakes reports zero issues. Recursive
  bytecode audit covers 262 code objects and 1831 LOAD_GLOBAL instructions; zero
  names are unbound in the actual module globals/builtins. This is not a proof of
  every dynamic attribute or runtime branch; production-path tests cover dispatch.
- Real helpers/build_plan constructs 6378 unique ordered test IDs / 235 modules.
  The first 6314 IDs and 233 groups exactly equal the parent plan. Actual own
  loaders contain 40 science and 24 infrastructure tests. Loading all 235 modules
  directly yields 6379 cases; the only set difference is the inherited exact ID
  tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state.
  No test bodies run during inventory construction and no new exclusion exists.
- Full ordered-ID SHA256 is
  76dfa4fd2952bdffd80250e57880d58cda72e7f7c16402c1817fed39ff294460;
  parent ordered-ID SHA256 is
  3ee31f196c842e57f786d5efe1c22df5460d41ddc92b86cf40d8c9f56209ac76.
- Manifest recomputation matches
  538150bd2b43ff286e4d5b0e0c1d665ea1e1c4d43cf8148cba1c5d1a4192734c.
- PowerShell 7.5.4 Linux Parser.ParseFile reports zero errors for active_v2,
  invoke_c342 and run_c342. Actual native user-side AST and path checks remain.
- CLI --help succeeds; own tests check rejected bad modes, command argument
  positions, plan/HEAD/module-index/role/folder binding and failure propagation.
  git diff --check passes and the reviewed tracked tree was clean.

Author environment: Linux Python3.12.14 / PyTorch2.10.0+cpu / NumPy2.3.5; two Torch
threads in science tests. Native registration remains Windows Python3.13.15 /
PyTorch2.10.0+cu130 / NumPy2.3.5, CPU float64, two threads. No native reinstall.

## Scientific path and fixed gate

The independent review compared accepted C326 balanced_allocation, family_mask,
exposure and select_tokens implementations with the new caller. Allocation uses
only original-family slot4 query-pair edges, fixed first-cycle length4 quotas
8/8/9 per profile and exact corresponding-event complement in cycle2. Pair rows
stay together. Every candidate row gets length4=25 and length5=25 per cycle; each
mixed update contains 5..8 pairs of each actual length. All five real schedules
are validated by author tests. No fallback, seed/profile selection or extra budget.

The selector changes only registered tokens, receives no labels, and feeds the
actual native model. The fitting path remains ordinary mean CE256, backward,
global clip1 and AdamW core_slow. Paired models have equal initial weights and
independent storage; one optimizer crosses the 1200/1201 boundary continuously.
All ten fits finish before evaluation. Checkpoints are independent detached copies.

Every actual token-and-target batch is hashed during fitting as little-endian
int64 and independently reconstructed from canonical banks/events/family and
length masks. The stream and bank recipes are both checked. Control/candidate
nonpadding tokens are 3225600/3168000 per model; equal update/row/padded budgets
do not imply equal token exposure or FLOPs. All256-class argmax/native_before,
114 views, exact argmax replay and 1e-9 drift remain unchanged.

The gate requires all five candidate full original2..6/interior4 gates; for EACH
seed and EACH of six domains, both HOLDOUT answer and query-pair gains >=0; and
strictly positive aggregate original4 gains for BOTH endpoints. Pooled short-domain
counts are descriptive and cannot hide a domain loss. Perfect-control saturation,
ties and one-endpoint-only improvement are valid negatives, not grounds for retries.

This is a new original4-retention comparison against fresh original5-only fitting.
It does not change C340's accepted negative or re-estimate its original4-versus5
six-character effect. Reducing original5 exposure and the fixed temporal assignment
are part of the intervention. It may not fix trained interior4 failures. No optimal
mixture, causal mechanism, arbitrary-length generalization, Gate F completion or
production adoption is claimed.

## Parent writer semantics, dispatch and protection

The accepted C341 writer is diagnostic. The child validates its exact primary and
envelope hashes, diagnostic PASS, capability_gate_applicable=false and nested
validation_summary.parent_validation_summary carrying C340 candidate_gate=false /
eligible_seed_count=2. It does not substitute a stale trained-parent summary shape.

Actual signatures and calls agree:

```text
C341.semantic_recheck(out341, out340, read)
C342.native_preflight(data_out, cx, root, pins, read)
C342.run_training(out, data_out, cx, root, pins, read)
C342.semantic_recheck(out, data_out, cx, read)
```

C342.previous() remains C332 and reference() remains C340. Immediate diagnostic
reconstruction runs under no_neural without recursively rerunning ancestor models.
The accepted canonical-data bridge and reader/schema meanings are preserved.

Inherited protection retains all 475 C341 outputs, including all 469 regression
proofs, then adds all seven OWN files: 916 sources = 909+7 and 7205 inputs =
6723+475+7. Explicit finite lease max_files=7205, initial hashes and all 7205 final
uncached rereads remain mandatory. A successor retains 481 C342 outputs.

Actual helper/context expansion and immutable source declarations cover 66
enumerated repository dependency files with zero uncovered dependencies. The
independent reviewer checked the C341/C340/C338/C337/C332/C331/C329/C326 bridge,
inherited OWN union and all 20 explicit helper BOOTSTRAP/FIXED pins against Git.
The source audit additionally follows canonical context/model aliases and their
matching PINNED/OWN/EXTRA declarations. Execution-HEAD reconstructability is never
used to excuse a missing explicit deciding-path dependency.

This author checkout lacks native runs/ artifacts. Neither reviewer nor root claims
to have rehashed the actual 909-entry C341 source map or all native parent input
bytes here. The accepted C341 verification evidence, immutable snapshot chain,
declaration audit and child structural tests establish the authoring contract;
C342 native snapshot/leases/final rereads enforce it against the real files.

Production-path ordering tests cover protection/parent semantics -> discarded
native preflight -> full regression -> fitting/evaluation -> guarded saved
reconstruction -> final rereads -> fresh verifier. Integrity failure stops; scientific
PASS and valid negative both require complete execution evidence. The fresh verifier
reconstructs saved metrics/input fingerprints; it does not replay all 24000 updates.

## Launcher, assertion audit and activation

The exact launcher/runner source targets used by string assertions were checked.
There are no getsource-based numeric count assertions or mistaken caller/callee
source checks; actual loaders enforce counts. Accepted tests remain unchanged.

Standard route is invoke_active_v2 -> invoke_c342 -> run_c342. Branch, tracked tree,
ExpectedHead, unique ACTIVE, dependency and AST guards precede log creation and
publication. Stale requests skip without execution or publication. The user block
parses the dispatcher, dispatcher parses the selected launcher, and launcher parses
itself/runner. Correct C342 prefix, log ID, Python path and CLI ordering are fixed.

Independent committed-byte review PASS and root's complete post-publication checks
authorize a separate docs-only activation. That commit adds this review, archives
the exact pre-activation handoff and updates authoritative handoff. All seven
reviewed source/preregistration blobs remain unchanged. Native full regression,
Windows read leases and ten-model scientific training are still NOT YET JUDGED.
