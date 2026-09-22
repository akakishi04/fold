# V5-F bias-update/query amortization v0.1

## Motivation and one question

C227's frozen-state comparator reused a checked full Cholesky factor and was faster than current
H1/H2 at all tested dimensions. Do not present C226's crossover against repeated factorization as
a general efficiency advantage.

C228 asks: on the same initial states, what are update-plus-query costs when observations are
replaced repeatedly, with1/4/16 queries between consecutive updates?

This changes the workload from one fixed final state to a fixed stream of bias-only replacements.
The required benchmark-local cache adapter preserves matrix-factor reuse across those replacements.
No production memory code, existing accepted benchmark, safety check or neural weight is changed.

## Dataset and dimensions

Keep C226/C227 dimensions2/16/64/256, update rank2, readout dimension2, two live factors, six registered
relations and the original32-event prefix. Start from the same current alpha/beta state.

Append events33..44 of the unchanged deterministic C224 ledger generator. These12 events replace
beta's semantic value cyclically. Both candidate and comparator use the same parsed events and
retain all44 original raw records and source byte ranges.

Prefix SHA256:
`735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921`.
Complete44-event SHA256:
`493140c7cbc874c90066da8defe3785a0b667f6c2e2edbdbcc2b55bd5e595f11`.

Queries per update are1,4,16. Twelve cells: four dimensions times three query frequencies.
Each trajectory starts from the original prefix, applies12 updates and makes12/48/192 queries per
arm. Every individual query result is validated, not merely the final state of each trajectory.

## Fair factor reuse across updates

The six existing relation contributions all use the same per-factor matrix contribution regardless
of semantic class. These replacements change the aggregate bias, not aggregate W. Rebuilding a full
factor on each such replacement would be an unnecessarily weak baseline.

The comparator therefore:

1. constructs the checked full Cholesky factor for the original current state;
2. after each symbolic state update, checks bridge/tensor stamps and exact equality of new aggregate
   W against a retained copy;
3. computes a finite new right-hand side and binds the retained factor to the new immutable state;
4. answers with the inherited C227 checked `query_cached()` path.

This is not answer memoization. The same factor object is retained; rhs/state binding is replaced.
A changed matrix, capability failure, mutated base/cache tensor or nonfinite rhs is rejected.
Matrix-changing updates, concurrency and mutations outside normal tensor-version tracking are out
of scope. The adapter is benchmark-local, not a general production cache.

Candidate path remains unchanged: apply MemoryOp, invoke the existing commit boundary, then
`ChunkedMemoryBank.read()`. Reference safety checks are not disabled.

## Timing protocol and accounting

One warm trajectory plus three measured trajectories per cell. Fresh initial states are built for
each trajectory. Arm order alternates by trial/step; no instrumentation runs in measured phases.
CPU threads2, float64 numerical path, deterministic algorithms. Three-trial medians are descriptive.

Record separately:
- shared numerical bank/bridge construction;
- initial index construction;
- candidate initial32-event state construction;
- comparator initial symbolic state construction and checked cache preparation;
- each arm's total update time and total query time;
- canonical export time.

Main comparison is the sum of measured update and query phases. Update phases include event parsing,
raw-byte append, source-index append, MemoryOp application, and candidate commit or comparator rhs
refresh. Query phases include every actual query call and result collection. Untimed validation and
trace passes are excluded equally.

Cold-inclusive totals are sums of the listed common/setup/update/query phases, not a stopwatch of
the entire application. The common numerical construction is included identically in both totals;
it is not hidden as a free baseline prerequisite. Harness bookkeeping, initial dictionary copies,
validation, output writing and export are not included in that sum. Export cost is separately shown.

Both arms retain complete raw/index/current state/shared bridge. The comparator additionally retains
L, rhs, aggregate-W equality guard and stamp metadata. Required extra numerical tensor storage is
8*(n*n+n+4) bytes. Shared comparator bridge still contains the unused compiled capsule, as in C227;
this is not an independently minimized comparator.

Canonical noncompressed exports and reachable-object/unique-CPU-tensor estimates are reported.
Audit snapshots/results retained solely for verification are not part of the logical serving-state
estimate. No peak process RAM/VRAM is claimed.

## Quality, controls and actual traces

Before streaming, both original arm export inventories must exactly match accepted C227 inventories
for that dimension. At every update require complete symbolic-state/provenance agreement and every
query output within1e-10 of untimed full_reference on the current state. Do not compare only labels
or permit old answers to pass after a replacement.

After the trajectory, run an untimed checked preparation and replay all12 refreshes on saved
immutable symbolic states. Capture actual cholesky/cholesky_ex/solve/cholesky_solve operations.
Require one initial factorization,12 rhs refreshes and zero update-time refactorizations in this
trace. Final query trace remains candidate cholesky2/cholesky_ex2/solve2 and cached cholesky_solve n.
This trace is separate from measured phases and cannot inflate their timing.

Validate unchanged query state, full raw/index coverage, stable final exports across repeats,
complete archive members/bytes and all protected source/input identities. Changed-matrix and
mutation rejections, unfavorable-cost acceptance and archive corruption are covered by authoring
tests.

## Interpretation

Measurement PASS means the comparison and quality/protection checks succeeded. It does not require
H1/H2 to be faster or smaller. Unfavorable costs remain unfavorable and must inform architecture
selection, rather than triggering threshold or baseline changes to obtain a win.

This stream tests values changing on a fixed numerical structure. It is not evidence about many
live factors, changing matrix structure, arbitrary queries, learned reasoning, language, acquisition
or full Gate F. Answer caching and matrix-specialized solvers remain possible stronger alternatives.
No Gate F completion is inferred.
