# V5-F stateful baseline attribution v0.1

## Motivation and question

C224 passed its measurement audit, but H1/H2 retained more bytes at every measured size. Avoiding
full-history replay reduced warm raw rereads; this alone does not establish a capsule-specific
advantage, because an ordinary incrementally updated symbolic state can avoid replay too.

C225 asks one question: with the same two live factors, raw history, source index and numeric bridge,
what does the current H1/H2 representation cost relative to retaining a plain current MemoryState
and solving the full numeric system from that state on each query?

## One changed comparator

H1/H2 candidate: exactly the accepted C224 candidate construction/query path.
New baseline: apply each original event once to MemoryState, retain the current state, and call the
existing MemoryCapsuleBridge.full_reference(state) on queries. Do not reconstruct that state from
raw history per query. This is a stateful comparator, not the replay comparator from C224.

There is no production optimization, learned-head inference, retraining, raw deletion or new task.
The C224 replay results remain historical context, not relabeled as stateful-baseline results.

## Matched retention

Both arms retain identical evidence.ndjson and source-index.json bytes. Both retain the same complete
numeric bridge object. Candidate additionally retains its bank/H1/H2 state; baseline retains its
plain MemoryState. The exports include all current records, revisions and provenance fields.

The shared bridge includes the compiled response capsule even on the full-solve arm, where it is not
used for answering. That common overhead is intentionally held fixed, not silently subtracted.
Therefore C225 is a conditional representation/query comparison with a shared bridge, not a claim
that the baseline is a minimal independently optimized implementation.

The full source index is still a benchmark sidecar, not a demonstrated bounded production index.
Its raw-byte ranges, source identity and current-record provenance are validated in both arms.

## Fixed data and measurement

Reuse C224 raw ledgers at8/32/128/512 events. Alpha remains the fixed anchor; beta cycles through
REPLACE. Only two current live factors and a two-dimensional numeric system are tested.
All four original ledger SHA256 values are fixed in the manifest.

Keep C224 float64 numeric tolerance1e-10; one warmup and three measured queries per arm/size.
Alternate arm order within each size. Timings are descriptive medians, not statistical speed claims.

Construction is measured separately: identical raw ledgers are processed once per arm to construct
current state. The H1/H2 arm uses its existing commit policy; the symbolic arm has no capsule-bank
commit. Record index construction and canonical export time separately. Do not compare warm query
latency while hiding construction work.

Queries receive current state, not raw history or a source index. Both warm raw-reread/event counters
must be zero. These counters describe the explicit instrumented data paths, not hardware I/O traces.
No many-factor scan bound or asymptotic query guarantee is inferred from two live factors.

## Quality and source parity

Compare complete current symbolic states, including provenance and revision fields, not just their
final numerical values. Require both numeric statuses SUPPORTED and max absolute response difference
at most1e-10. Queries must leave both retained states unchanged.

C225 loads and validates the real C224 measurements artifact. The new H1/H2 candidate's three file
inventories must match the accepted parent candidate byte-for-byte at all four sizes. Parent timings
are not required to repeat. This prevents an unregistered change to the candidate while introducing
the stronger comparator.

## Cost accounting

Candidate exports: original raw, full source index, complete state-and-bank JSON.
Symbolic exports: identical original raw, identical full source index, complete state-and-bridge JSON.
Use C224 canonical uncompressed serialization. Retain a ZIP_STORED audit archive, verify its complete
member set and independently reread every member to check actual bytes and hashes.

Report component/total export bytes, candidate-minus-symbolic byte deltas, and separately labeled
reachable-object/unique-CPU-storage estimates. These are not native checkpoint sizes, allocator
reservations, process RAM/VRAM peaks or total application memory. Neural model memory is not measured.

## Verdict

Measurement PASS requires all four sizes, exact input identities and inventories, matched raw/index
retention, full symbolic/provenance and numeric parity, unchanged states, and no warm raw replay in
either arm. Candidate storage or latency superiority is NOT a PASS requirement.

Report candidate-to-symbolic median query ratios without changing thresholds after observing them.
A value greater than1 means the candidate was slower in that descriptive measurement. Report larger
candidate storage without converting an audit PASS into an efficiency success.

A complete measurement that misses a registered correctness/accounting criterion is scientific FAIL.
Source/artifact/schema/manifest/regression/incomplete-run defects are INVALID / RETRY SAME C225.
Gate F is not decided here. No C226 until C225 is formally judged.
