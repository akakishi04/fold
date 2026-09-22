# V5-F checked reduced preparation reuse v0.1

## Motivation and one question

C229's representative n256/q16 profile placed78.36% of candidate query cumulative work inside
ResponseCapsule.response, including its nested operations. It showed192 Cholesky checks,
192 cholesky_ex checks and192 solves for192 queries on a matrix-invariant workload.
These are instrumented diagnostics, not speed evidence or guaranteed removable time.

C230 asks whether reusing verified W-dependent reduced preparation improves the same unprofiled
update/query workload without changing answers, state semantics, safety conditions or comparators.
This is one optional implementation change, not another search for a favorable task.

## Optional path, unchanged reference

Add `fold_lm/v05/prepared_capsule.py`; do not edit ResponseCapsule, memory_bank, old benchmarks or
accepted tests. It is explicitly CPU float64, unbatched, inference-only. It is not installed as the
default serving path or used for training.

The reference equation remains:

```text
M = I + W K
rhs = current_bias - W g
answer = y0 + V solve(M, rhs)
```

Preparation checks finite tensors, shapes, exact W symmetry, Cholesky(K), and positive-definiteness
of I+L.T W L. It then factors the generally nonsymmetric M using pivoted LU and stores W,LU,pivots.
No inverse, final answer, or observation bias is cached.

Each query verifies capsule identity, tensor identity/version and inference flags, unchanged base/
registry context and exact equality of current aggregate W with the retained W. It checks current
bias finiteness, performs lu_solve using that current bias and checks output finiteness. The benchmark
still runs bank._read_parts and constructs the same BankRead metadata/finite-checked cloned value.

Changed W or capsule/context/cache mutation is rejected as stale preparation; the caller must
explicitly prepare again. There is no silent full-solve fallback or check=False route. Numeric
unsafe inputs fail closed. The original reference API retains its previous status/error behavior;
the new opt-in numeric API uses explicit exceptions for unsupported/stale preparation.

Normal PyTorch mutations and object replacement are guarded. External writes via unsafe aliases,
.data changes, concurrency, autograd and batched operation are outside this initial contract.
Exact symmetry is stricter than the reference's allclose tolerance, not weaker.

## Same workload, three arms

Reuse the C22832-event prefix and12 bias-only replacements, dimensions2/16/64/256, bursts1/4/16,
two live factors, two update coordinates and two outputs. Matrix W stays identical across updates.

- candidate: unchanged H1/H2 apply/commit/read;
- prepared: identical apply/commit, optional prepared numeric response on query;
- cached: unchanged C227/C228 full Cholesky reuse with rhs refresh and validity checks.

Each trajectory starts from the same prefix. Three-arm order rotates by trial+update. One warm
trajectory and three measured trajectories per cell. No profiler runs in these timing regions.
Every current query answer is compared with an independent full solve within absolute1e-10;
all three symbolic states and provenance are checked after every update.

C229 measurements and quality-check artifacts form the parent adapter. The latter stores the final
candidate/cached inventories under `inventory`, not `retained_inventory`. Check their actual parent
schema, mode-specific quality records and ordered12-cell identities before measurement.
The original two final export inventories must match C229 exactly. Prepared base exports must match
the original candidate; its new cache is a separately counted file.

## Accounting

Retain complete raw evidence, identical byte-range source indexes, current state, full numeric bridge
and all caches in their respective arms. Prepared cache holds rank2 W and LU (32B each), plus int32
pivots (8B):72 additional numerical bytes. Binding/version metadata is additionally included in
canonical export and reachable-object estimates. This is not72B for the entire memory system.

Measure common numerical setup, index build, each initial state, each cache preparation, update,
query, stream and export separately. Stream means update+query phase totals. Cold-inclusive totals
add the same common numeric/index setup and arm-specific initial construction/preparation; they
are not application wall-clock or TTFT. Initial dictionary copies, correctness oracles, snapshots,
trace wrappers, report construction and export are excluded from timed stream/cold phase sums;
export is separately reported.

Record resident estimates for each arm's reachable objects and CPU tensor storage, not process peak
RAM/VRAM. Archive format is noncompressed ZIP containing canonical audit exports, not an optimized
production serializer. Sharing across arms is not used to reduce any individual arm's accounting.

## Trace and safety evidence

Outside timing, verify preparation invokes Cholesky2, cholesky_ex2 and LU-factor2. Verify prepared
queries invoke only LU-solve2; original queries retain Cholesky2/cholesky_ex2/solve2; full cached
queries retain cholesky_solve n. Query guards remain live. Both prepared and full factors keep their
identities across the12 updates. Wrappers are restored even on errors.

Unit tests exercise signed safe W, non-SPD/nonfinite/nonsymmetric rejection, changed W, base/capsule/
cache/pivot mutation, changed inference flags, fresh bias rather than answer memoization, numerical
agreement with the exact fetched reference source and full solves at four dimensions.

## Interpretation and stop

Audit PASS requires all quality, parent-export, cache-byte and trace conditions, not a speedup.
Report unprofiled speed ratios versus both the original path and the strong full-cache baseline,
including cache preparation/storage costs. Unfavorable results stay unfavorable.

After this bounded intervention, decide whether to adopt it only in the supported serving scope,
restrict H1/H2's role, or stop this local optimization track. Do not indefinitely add favorable
workloads instead of returning to whole-model/language/reasoning evaluation.
No Gate F completion, general cache correctness, matrix-changing performance, many-factor indexing,
natural-language capability or model-wide speedup is implied.
