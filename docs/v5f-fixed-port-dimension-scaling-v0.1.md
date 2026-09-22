# V5-F fixed-port numerical-dimension scaling v0.1

## Motivation

C225's measurement audit passed, but the existing H1/H2 reference used more retained export bytes
and had slower descriptive query medians than incremental symbolic state at all four history sizes.
Ordinary state retention also eliminated full-history replay. This is an unfavorable result for a
capsule-specific efficiency claim in that measured configuration; it is not relabeled as a win.

The full numerical system was2x2 and the update rank was2, so there was no reduction in solve
dimension. C226 varies the full numerical dimension while preserving two update coordinates, two
readout coordinates, two live factors and the same stateful comparator. No production optimization.

## One question

With update/readout rank2 fixed, how do the existing checked H1/H2 and retained-symbolic/full-solve
paths compare as the coupled numerical system grows from2 to16,64 and256 variables?

These dimensions describe the numerical memory system, not neural layers, model parameter counts,
number of semantic concepts, or number of live memory factors.

## Fixed and changed conditions

Only the full-system matrix family/dimension changes. History is fixed at32 events, using the exact
C225 ledger: fixed alpha plus cyclic beta replacements, two final observed factors.
Original raw SHA:
`735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921`.

Keep the original six relation contributions, operations, source IDs, scope/revision/provenance,
readout dimension2, update rank2 and float64 tolerance1e-10. No learned model is called or trained.

At n=2, return the original C216 bank factory unchanged. Both exported arm inventories must match
the accepted C225 n=2/history32 measurement byte-for-byte. Timing is remeasured, not forced to match.

For n>2, use a symmetric matrix with diagonal4 and off-diagonal -0.25 on edges
(1,2),(2,3),...,(n-2,n-1) and (0,2), using zero-based coordinates. Coordinates0/1 are the visible
ports. Every hidden coordinate connects to them through this graph; no disconnected padding is
appended. eta is zero; U selects the first two coordinate axes and Q is U transposed.

The matrix is strictly diagonally dominant with positive diagonal; the reference compiler still
performs its actual SPD checks. U has full column rank. Tests verify connectivity and that the hidden
system changes visible numerical response. There is no jitter, check=False or silent fallback.

This is a deliberately declared sparse, coupled matrix family evaluated using the existing dense
full_reference implementation. It does not claim superiority over specialized sparse/banded solvers
or optimized factorization/update caches.

## Reused measurement and fairness

Reuse C225.measure and C224 helpers without editing accepted sources. A local backend-factory adapter
constructs the dimension-specific bank; a helper delegate captures the actual built state for later
instrumentation. Neither adapter is a learned component or a production runtime modification.

Candidate: unchanged ChunkedMemoryBank.read.
Comparator: unchanged incremental MemoryState, maintained once per event, then bridge.full_reference
per query with no raw replay. Both retain the identical full evidence, source index and complete
numeric bridge. The common bridge includes its compiled capsule even on the full-solve arm.

Higher-dimensional candidate construction includes the small original bank template plus the new
bridge compilation. This overhead is not omitted. Report construction and index/export work
separately; do not present warm-query latency as total lifecycle cost.

One warmup and three measured queries per arm/dimension, alternating order, CPU threads2 and
deterministic algorithms. These are descriptive medians, not statistical speed claims. No timing
threshold, dimension selection after results, or storage-superiority gate.

## Actual solve-size audit

After timed queries, instrument one extra query per arm by temporarily wrapping torch.linalg
cholesky, cholesky_ex and solve. Record each actual matrix shape; restore functions even on errors.
This instrumentation is outside timing and does not remove or replace the underlying operations.

Expected H1/H2 trace for every n:
`cholesky(2x2), cholesky_ex(2x2), solve(2x2)`.

Expected symbolic trace:
`cholesky(nx n), solve(nx n)`.

Require the instrumented outputs to match within1e-10 too. The trace establishes the actual numerical
work shape, not a bound on all state scans, all memory access or whole-model inference.

## Complete retained cost accounting

Export the same canonical audit format as C225. Both arms retain raw evidence/index; candidate exports
complete bank/state, symbolic exports complete bridge/current MemoryState. Include the full original
J/eta/Q/U and compiled response data. Do not report only a small2x2 payload as total memory savings.

Write ZIP_STORED audit exports, verify all member names, actual bytes and SHA256 values. Report total
export bytes and component sizes plus separately labeled reachable-Python/CPU-tensor estimates.
These are not native checkpoint sizes or process/allocator RAM/VRAM peaks.

The extra dimensions increase retained full-bridge memory in both arms. C226 does not discard the
full matrix or raw evidence to manufacture storage superiority.

## PASS and interpretation

Audit PASS requires all four registered dimensions; exact matrix/raw identities; original n=2 arm
exports; inherited full symbolic/provenance/numeric parity and state non-mutation; matched raw/index
retention; zero warm raw reread for both arms; complete export inventories; and exact actual
linear-algebra traces with numerical parity.

Store positive or negative storage deltas and query-time ratios independently of this gate.
A positive result would establish only a conditional advantage over this stateful dense full-solve
reference at these dimensions. A negative result remains negative. Neither passes Gate F.

No many-live-factor indexing, natural-language task, neural inference, acquisition, joint training,
concurrent/cache freshness or independently optimized comparator is evaluated here.
