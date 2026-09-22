# C227 preregistration — checked factor reuse attribution

**C226 ACCEPTED PASS. C227 ACTIVE / NOT YET JUDGED. C228 NOT REGISTERED.**
Gate E PASSED. Gate F NOT PASSED.

## One scientific question

On the same C226 frozen final states and numerical dimensions, how does the unchanged H1/H2
representation compare with a full-system baseline that reuses its checked Cholesky factorization?

Only one new comparator is added. Keep the candidate and the original full-solve reference unchanged.
No training, new semantic task, production optimization, answer cache or Gate F decision.

## Accepted parent and evidence

Scientific execution HEAD: `17284250b25bdb5160d5d3ffa95501a4f5070e03`.
Published log commit: `2e4d4c01a9c37409cf4ebbc6c620c748b61e6156`.
Summary SHA256: `ba4465c8c84e8fd54da1f7096a18056b7e53e6689a6ba3df5e1f9c559a7fac08`.
Validation SHA256: `ec05f980af138ef10f243c2a75788d50f7322f47bd5b8309b7e896c398ccaad7`.
Measurements SHA256: `f312af884dc6ee11bf02bf8b1aa3022531b3d599307571172557abc242519f44`.
Local summary:
`runs/c226-v5f-dimension-scaling-b1186f4e625e45e0909c44ed8c585937/summary.json`.

Read and validate all parent artifacts,196 parent source pins and256 inherited protected inputs.
The child adapter validates the parent measurement order and its registered row gate. Compare actual
candidate_files/symbolic_files inventories against the accepted measurements at every dimension.
No timing from C226 is silently reused as a C227 measurement.

Acceptance and limitations: `docs/experiment-ledger-addendum-c226-c227.md`.

## Fixed data and arms

Numerical dimensions2/16/64/256; history32; two live factors; update/readout rank2;
C226 matrix factory unchanged; raw hash
`735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921`.

Arms:
- candidate: existing checked H1/H2 bank.read;
- symbolic: current MemoryState plus existing checked full_reference;
- cached: same symbolic state/full bridge plus checked full Cholesky factor and updated rhs.

All three retain identical raw/index bytes and the complete bridge. The cached arm adds its factor
and rhs storage; it does not discard raw history or provenance. Preparation is timed separately.

The cached query checks exact state/bridge binding and tensor identity/version stamps. It uses
cholesky_solve and never refactorizes. State is frozen during queries; this is not a production cache
invalidation or concurrency test. No inverse, jitter, answer memoization or disabled safety check.

## Fixed measurement and PASS gate

CPU threads2, deterministic algorithms, float64 reference, absolute error tolerance1e-10.
One warmup and three measured queries per arm/dimension; cyclic order rotation.
Require three-way finite response parity, identical current symbolic state/provenance, no retained
state/cache mutation, complete raw/index retention and zero warm raw-history work.

Untimed trace requirements:
- candidate query: cholesky2 /cholesky_ex2 /solve2;
- original symbolic query: cholesky n /solve n;
- cache preparation: cholesky n;
- cached query: cholesky_solve on n*n factor, no refactorization.

Require exact two-arm parent export parity and additional cache tensor storage8*(n*n+n):
48/2176/33280/526336 bytes. Count cache metadata, complete state/bridge and reachable-object overhead
separately. Verify every archived member's exact bytes/hash. Five outputs, all under ignored runs/.

Audit PASS does not require speed/storage superiority. Unfavorable costs remain unfavorable.
Complete quality/measurement gate misses are scientific FAIL; source/artifact/schema/execution defects
are INVALID / RETRY SAME C227. No C228 before formal C227 judgement.

## Authoring registration

OWN6:
- `fold_lm/v05_benchmarks/gate_f_c227_factor_reuse.py`
- `tests_lm/test_v05_c227_factor_reuse.py`
- `tools/run_c227.ps1`
- `tools/invoke_c227.ps1`
- this preregistration
- `docs/v5f-checked-factor-reuse-v0.1.md`

Source pins202. Protected inputs268 = parent256 + parent summary/artifacts6 + OWN6.
Direct dependencies25: inherited C226 deciding dependency set plus C226 benchmark.
No accepted source/test/log/dependency is changed, moved or removed.
Outputs5: reuse-plan.json, reuse-exports.zip, measurements.json, quality-checks.json,
validation-summary.json.

New tests32; modules112; loaded2562 /focused2561. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Manifest SHA:
`4ea370a98b04bff4364f2ec8dccbc5fff658c1d4529a13ee6c3fc1d0c0cfa23d`.

## Post-authoring review

`post_authoring_review = PENDING`

Author-side30 targeted tests passed before remote review (1.368 seconds),32 methods enumerated,
manifest matched and all three embedded Python runner blocks compiled. Tests include real PyTorch
Cholesky/cholesky_solve versus solve on synthetic bridge fixtures at all four dimensions, stale
binding/tensor-mutation rejection, trace restoration, exact archive contracts, and a synthetic run
exercising parent-adapter/measurement/export/postcheck ordering.

Those fixtures are not the complete accepted memory backend. Not executed locally: test31 with the
actual parent bank/exports, test32/full2561 historical suite, Windows PowerShell AST parse, local
parent-artifact precheck or formal C227 measurements. Repository clone failed DNS resolution.

Before review PASS, re-fetch committed code/test/runner/launcher and verify exact Git blobs against
the tested copies, rerun targeted tests, check direct dependency/protection coverage, parent field
semantics, original export parity paths, CLI indexes and all launcher guards. Review PASS must state
its scope and must not misrepresent synthetic testing as complete historical execution.

The authoritative runner executes all32 own tests, then2561 focused tests, then measurement.
Failure stops before the next phase; the console log is published through the standard mechanism.

## Interpretation boundary and stop

Three-trial timings are descriptive. Canonical exports and reachable data are not native checkpoints
or peak process RAM/VRAM. Shared symbolic bridge includes the unused compiled capsule. Identical
answers could also be memoized; factor reuse is not an optimal baseline. No matrix-specialized sparse
solver, many-factor query, natural-language task or learned model is evaluated.

Use the active dispatcher and final reviewed HEAD. Judge C227 before C228.
No cleanup, history rewrite, new CI or Actions-storage work. Gate F remains NOT PASSED.
