# V5-F checked factor reuse v0.1

## Question

With the same C226 matrices, final memory states, evidence and readout/update rank2, does the
unchanged H1/H2 query retain a measured advantage over a full-system baseline that reuses a checked
Cholesky factorization?

C226's n256 crossover was against a full Cholesky safety check plus separate dense solve on every
query. It did not establish a win against factorization reuse. C227 adds that comparator; it does
not optimize the accepted candidate or claim a general speed/storage win.

## Held constant

Numerical dimensions2/16/64/256, history32, two live factors, update rank2 and readout2.
Use the exact C226 factory/matrix family and C224 raw ledger. Raw SHA:
`735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921`.

All candidate and original symbolic export inventories must equal their accepted C226 counterparts
at every dimension, including exact bytes/hashes. No accepted source is edited.

No neural inference/training, production module change, arbitrary new query, live-factor scaling,
answer memoization, retention change, sparse solver or Gate F decision.

## Three arms

1. `candidate`: unchanged ChunkedMemoryBank.read with existing safety checks.
2. `symbolic`: unchanged current MemoryState plus bridge.full_reference per query, without raw replay.
3. `cached`: same current MemoryState and full bridge plus a precomputed full Cholesky factor L and
   updated right-hand side. Query uses Q @ cholesky_solve(rhs,L).

The cached arm aggregates the actual current observed relations, reconstructs the full updated
matrix, rejects nonfinite inputs and performs checked Cholesky once. It does not use an inverse,
jitter or an unchecked factorization. Preparation time is recorded separately from warm queries.

The query helper binds to the exact same state and bridge objects and checks tensor identity/version
stamps, including registry contributions, L and rhs. It rejects changed bindings and ordinary
in-place tensor changes. This is a benchmark snapshot cache, not a production cache-invalidation
mechanism: direct bypass mutations, concurrent changes, arbitrary replacements and cross-process
serialization/resumption are outside scope. No state update occurs during the repeated queries.

## Fair retention and accounting

All arms retain identical raw evidence and source-index bytes plus the complete bridge. The bridge
includes an unused compiled capsule in both symbolic arms; no independently minimized baseline is
claimed. The original symbolic export remains intact and the cached arm adds factorization-cache.json.

The cache export stores L, rhs, state revision metadata and tensor versions. State/bridge references
are represented by the already-counted state-and-bridge.json rather than duplicating the full objects.
Object addresses are not portable data. Reachable-runtime estimates separately traverse the complete
cache object, its stamps and referenced objects with identity-based deduplication.

L occupies n*n float64 elements and rhs occupies n, so additional retained tensor storage must be
8*(n*n+n) bytes:48/2176/33280/526336 bytes for the registered dimensions. Do not report these tensor
bytes as total cache cost: export metadata and reachable Python-object overhead are also reported.

Exports are canonical noncompressed audit data, not native checkpoints. Reachable-data estimates are
not process peaks. Peak RAM/VRAM remain unmeasured and explicitly null. Temporary matrix preparation,
allocator and library overhead are not represented by the retained snapshot estimate.

## Measurement order

Build raw/index, candidate state and symbolic state through inherited helpers. Record index build,
candidate construction, symbolic construction and extra cache preparation separately. Candidate
construction includes the shared bridge/compiler and the n2 template as in C226; symbolic construction
uses that bridge. Do not compare these split stage timings as independent cold-start totals.

One warmup plus three timed queries per arm/dimension; rotate the starting arm so each arm starts
one measured trial. CPU threads2, float64 numeric data, deterministic algorithms. Timings are
exploratory/descriptive. No threshold demands that any arm win.

Every timed query is checked for three-way response parity within absolute error1e-10. Compare full
symbolic state and provenance, verify retained source ranges and require state/cache non-mutation.
All three warm paths avoid raw-history processing. Zero rereads are structural path accounting,
not hardware disk-I/O counters.

Extra untimed instrumentation captures actual preparation/query calls and restores original functions:

| Path | Required numerical calls |
|---|---|
| H1/H2 query | cholesky2, cholesky_ex2, solve2 |
| Original symbolic query | cholesky n, solve n |
| Cache preparation | cholesky n |
| Cached query | cholesky_solve with n*n factor; no refactorization |

Instrumentation is never enabled inside timed trials. Reconstructing a second cache for the untimed
trace is validation overhead, not charged again as a normal query or retained cache.

## Audit PASS

Require all four sizes, unchanged C226 original inventories, complete cache exports/archive
readback, exact extra tensor sizes, expected traces, no raw replay, current-state/provenance/numeric
parity and no state/cache mutation. Quality or contract disagreement cannot be hidden by speed.

Audit PASS is independent of measured superiority. A cached baseline that is faster, larger, smaller
or slower is reported as measured without changing the gate. Full source/artifact/parent prechecks
and historical regressions remain mandatory.

## Limits and next decisions

This is frozen-state factorization reuse, not an update-heavy workload or an optimal comparator.
Repeated identical final answers could themselves be memoized; that is explicitly not implemented.
The sparse matrix family is still processed by dense kernels. No natural-language quality, model
intelligence, arbitrary-port capability, bounded many-factor retrieval or total-memory-cost Gate F
claim follows. Choose the next intervention from these results rather than predeclaring victory.
