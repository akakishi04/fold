# C224 preregistration — raw-retaining history cost audit

**C223 ACCEPTED PASS. C224 ACTIVE / NOT YET JUDGED. C225 NOT REGISTERED.**
Gate E PASSED. Gate F NOT PASSED.

## One scientific question

With two live factors and an increasing revision history, how do the existing H1/H2 reference and
full-history replay compare in retained memory-backend bytes and warm-query raw reread work when
original evidence, provenance and source lookup metadata are counted?

This is a measurement/attribution pilot. Measurement PASS is explicitly not storage superiority.
No production code changes, learned head inference/training, compression, acquisition or cleanup.

## Accepted parent and protected execution context

C223 scientific HEAD: `cdcc1d4211a149003f44dbdbd18a7e5367c013ab`.
Published log commit: `6e96f798b4c931247f58ab9982b617780d0ee9db`.
Summary SHA256: `1b08cf76a1c233ce849f2b7fe81dbb7fa44120e59a75b32e2f42c4ebccdad2ca`.
Validation SHA256: `b52c9d95bb89dca5061d2ccff4aab90276ea5dc4edba2d653b1d9fdc03d12db2`.
Local summary:
`runs/c223-v5f-request-freshness-56cfd6d212764ccf98e7789aa964de52/summary.json`.

Validate the accepted parent result, all178 parent source pins,220 inherited protected inputs and
all five C223 artifacts. The parent remains the execution-provenance anchor; no old decision labels
are reused as C224 answers. Reuse C220's existing helper chain to the accepted C216 bank and C213
MemoryOp semantics. Baseline full-reference solves aggregate the replayed current records, rather
than reusing the candidate H2 W/b.

The scientific paths call only protected repository helpers. Include state.py and capsule.py explicitly
in the dependency audit; they are already parent-pinned. Neural checkpoints remain protected but are
not loaded, trained or claimed to contribute model-memory comparisons in this isolated audit.

## Fixed workload

History counts8/32/128/512. Exactly two live factors: alpha class1 anchor and beta initially class0,
then cyclic REPLACE operations class1/class2/class0. Source IDs/times/scopes and raw UTF-8 text are
fixed by ledger(). SHA256 per size is part of the manifest. All typed operation kinds are oracle;
no natural-language extraction is evaluated.

Candidate: ingest events once into the accepted H1/H2 bank and commit each event (COMMITTED or
NOOP after a committed-factor replacement). Retain full raw history, a benchmark source-to-byte-range
sidecar index, and complete bank/current-state metadata.
Baseline: retain the identical raw history and same numeric bridge, but replay all events into a
fresh MemoryState on each query and invoke full_reference(). No current-state cache or source index
is retained by the baseline.

One warmup and three recorded queries/arm/size, alternating arm order. Both arms therefore have
16 query invocations over four sizes (4 warmups +12 measured). Time generation, index construction,
candidate ingestion/commit, canonical export and query medians separately. No timing threshold.

## Exact measurement definitions

Uncompressed canonical export files:
- candidate: evidence.ndjson, source-index.json, state-and-bank.json;
- baseline: evidence.ndjson, bridge.json.

Report exact file lengths and SHAs plus per-arm sums. Serialize every dataclass/object field, tensor
shape/dtype/value, raw event text, source ID and provenance. W/b tensor payload is a separate metric,
not the total. Unknown export types are rejected instead of silently omitted.

Store actual bytes in memory-exports.zip using ZIP_STORED and verify every archived entry against the
inventory. Per-arm totals exclude archive packaging; the archive file itself has its own length/hash.
This canonical representation is an audit export, not a native restart checkpoint or optimized binary
format. The sidecar index is benchmark-defined, not an existing deployed production index.

Report an estimated reachable-data resident size with Python object and unique CPU tensor-storage
deduplication. Do not label this process RSS or a peak. Peak process RAM/VRAM are explicitly null;
allocator, library and shared neural-parameter overhead are not measured. No total application RAM or
end-to-end learned-stack memory claim is supported.

## Fixed audit PASS gate

All four sizes must have:
- identical final symbolic state between candidate and raw-history replay, including provenance;
- SUPPORTED numeric answers, max abs error <=1e-10;
- two current live factors and unchanged query state;
- complete validated source index and current provenance resolution;
- identical raw evidence in both retained arms;
- exact complete file inventories and summed costs;
- candidate warm raw events/bytes reread0;
- baseline measured raw events rereadN and raw bytes rereadthe entire ledger every query;
- no new training or learned head forwards.

Report storage delta/ratio and storage_smaller_sizes separately. A larger candidate is compatible
with audit PASS and must not be called a compression win. Retaining raw evidence and adding state/
index represents a storage-for-query-work tradeoff. No success gate is tuned to favorable storage or
latency results.

Complete but parity/accounting gate-missing result: scientific FAIL. Missing parent/input/schema,
nonfinite or incomplete execution: INVALID / RETRY SAME C224.

## Authoring registration

OWN6:
- `fold_lm/v05_benchmarks/gate_f_c224_history_cost_audit.py`
- `tests_lm/test_v05_c224_history_cost_audit.py`
- `tools/run_c224.ps1`
- `tools/invoke_c224.ps1`
- this preregistration
- `docs/v5f-history-cost-audit-v0.1.md`

Source pins184 =178+6. Protected inputs232 =220+6 parent summary/artifacts+6 OWN.
Dependency coverage22: C220 direct set14 plus C220 benchmark, memory_dispatch, C221/C222/C223
benchmarks, memory_request_lease, state.py and capsule.py.

Outputs5: cost-plan.json, memory-exports.zip, measurements.json, quality-checks.json,
validation-summary.json. Raw artifacts stay under ignored runs/. The runner mirrors measurement
text into the published console log so the next review can inspect actual cost values remotely.

New tests30; modules109; loaded2466 /focused2465. Keep only the inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.
No accepted source, test, dependency or prior log is modified/deleted.

Manifest SHA256:
`0097887642e62a0c2e332d6b68a6dbcb769e829a1970387c3e0aa4ad28343103`.

## Post-authoring review

`post_authoring_review = PENDING`

Author-side28 targeted tests passed, including the measurement function exercised with a synthetic
backend at all four registered history lengths, raw/index UTF-8 bookkeeping, exact export totals,
provenance checks, deduplicated tensor-storage estimates and negative accounting controls.
Python source and three embedded runner blocks compile;30 methods enumerate; manifest hash matches.

Not yet executed here: test29 with the accepted numeric backend, test30/full historical2465 suite,
Windows PowerShell AST parsing, local parent artifact precheck or the authoritative C224 run.
A repository clone was attempted but DNS resolution failed. No mock-backend result is represented as
accepted numeric-backend execution or scientific evidence. The real runner executes all30 own tests
first, then2465 focused tests, then the audit. Existing numeric/production sources remain unchanged.

After committing all files, re-fetch remote code/test/runner/launcher, compare their blobs to the
executed copies, review parent semantic/helper contracts and the source/protection union, and record
the reviewed HEAD and explicit execution limits. Review PASS is required before an execution command.

## Limits and stop

This is revision-history scaling with two live factors, not many-factor indexing, native model RAM,
large-scale natural-language quality or cost superiority. Raw evidence is retained, never silently
deleted to manufacture savings. Gate F remains NOT PASSED. Judge C224 before C225 registration.
