# V5-F raw-retaining history cost audit v0.1

## Purpose

After C223, stop extending request-safety wrappers for this checkpoint and measure the outstanding
memory-cost boundary. Correct behavior is not evidence of small total storage.

C224 asks: with two current live factors and a growing revision history, what does the existing
H1/H2 reference cost compared with replaying the entire raw history, when retained evidence,
source lookup metadata, provenance and the complete numeric backend are counted?

This is an attribution/measurement pilot, not an optimizer, compression experiment or Gate F decision.
Measurement PASS does not mean that the candidate has smaller storage.

## Fixed history workload

History event counts8/32/128/512. Each prefix starts with observed alpha=class1 and beta=class0,
then REPLACE changes beta cyclically through class1/class2/class0. There are always two live factors.
Operations, source IDs, times, scopes and relation keys are deterministic and identical across arms.

Each event retains UTF-8 source text and typed operation fields in a canonical NDJSON ledger.
The Japanese text is illustrative evidence, not a natural-language parsing task. The existing
structured operation contract is used directly; no neural head is evaluated or retrained.

The history-length variable is not the live-factor-count variable. C224 does not demonstrate
bounded lookup over a large number of simultaneously live factors.

## Compared arms

### Raw-retaining H1/H2 candidate

Replay the events once into the accepted C216 numeric bank / C213 semantics / C215 H1/H2 path.
Commit after each event; a REPLACE of a committed factor can produce a NOOP commit. Retain:

- the entire original evidence ledger;
- an explicit source-ID to UTF-8 byte-range index;
- current H1/H2 state, factor metadata, clocks and provenance;
- the complete bank and numeric bridge, including J/eta/Q/U, relation registry and response capsule.

The source lookup index is a benchmark sidecar, not a claim that a new production index exists.
It is actually constructed and validated against all retained source bytes; current record provenance
is resolved through it. Its construction, contents and storage are included rather than treated as free.

Warm queries read the accepted bank state without reading the old raw ledger. Initial event ingestion
and index construction are reported separately, not hidden in the warm-query number.

### Full-history replay baseline

Retain exactly the same raw evidence bytes and the same numeric bridge. Do not retain a current
MemoryState or source index between queries. Every query parses all event records, applies the
accepted MemoryOp semantics, then invokes the bridge's independent full-system solve on the final
live records. All source/provenance data remain available by scanning the retained history.

This deliberately simple baseline is not an optimized latest-value index or a Transformer benchmark.
Both arms retain the common numeric bridge; no favorable reduction of the candidate's shared
infrastructure is made.

## Quality and interpretation

Require the candidate state and replayed symbolic MemoryState to agree, including clocks, factors,
relations and provenance. Numeric readouts must both be SUPPORTED with maximum absolute error
at most1e-10. Querying must not mutate the retained state. Keep current provenance resolvable.

The retained-raw candidate adds current state and an index to the same source history; this layout
should not be described as a storage compression win. Its potential benefit is avoiding repeated
raw-history work. Report the actual extra storage and actual avoided replay bytes separately.

## Storage measurement definitions

Produce actual uncompressed canonical audit exports per size and arm:

```text
candidate/evidence.ndjson
candidate/source-index.json
candidate/state-and-bank.json
baseline/evidence.ndjson
baseline/bridge.json
```

The serializer enumerates all dataclass/object fields, includes tensor shape/dtype/values and rejects
unknown types or nonfinite values. No current factor/provenance or base matrix is silently omitted.
Count exact UTF-8 file bytes, not only W/b tensor bytes. Also report the W/b payload separately to
show why a small numeric payload is not the whole retained memory.

Archive these files in a local ZIP_STORED artifact and read each entry back to verify length and SHA.
Per-arm totals exclude ZIP packaging overhead; the archive's own total length/hash is separately
registered. These are canonical audit exports, not native production checkpoint sizes or a restart
format. Text-vs-binary representation differences remain a limitation.

Estimate reachable data memory separately with deduplicated Python object sizes and unique CPU
tensor backing stores. This is not measured process RSS, allocator usage or a peak. Process peak
RAM/VRAM are explicitly unmeasured/null. Framework code, allocator caches and neural checkpoint
parameters are not loaded/counted as part of this isolated memory-backend experiment. Do not report
these figures as total application RAM or end-to-end learned-stack memory.

## Query-work and timing measurement

Per size and arm: one warmup, then three recorded queries; alternate candidate/baseline order.
For the baseline, count actual raw byte requests and parsed events in the replay iterator.
The candidate query takes bank/state and does not replay raw evidence; its raw-event counters are0.
The source is separately reviewed for hidden replay. The fixed two-factor metadata scans are not
claimed to be a general constant-time many-factor query implementation.

Report raw ledger generation, index build, candidate ingestion/commit, canonical export and query
wall-clock separately. Three-trial medians are descriptive; no timing threshold, speedup claim or
statistical significance gate is registered. Persistence/CPU data estimates do not include transient
peak work from replay or artifact export.

## PASS gate and next decisions

A completed audit passes when all four sizes are measured; state/numeric parity is preserved;
source index/provenance resolves; both arms retain the same raw bytes; exact inventories/totals match
actual exports; candidate warm raw rereads are0; and baseline rereads all N events and all raw bytes
on every measured query. Higher candidate storage is allowed and reported, never relabeled a win.

No production sources, checkpoints, accepted tests or old logs change. No new training, acquisition,
cleanup, CI or Actions-storage work. This pilot informs the next design decision but does not pass
Gate F or demonstrate a large-memory or natural-language advantage.
