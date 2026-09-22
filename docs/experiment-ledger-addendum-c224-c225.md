# C224 acceptance and C225 comparator boundary

## Formal verdict

**C224 ACCEPTED PASS (measurement audit). Storage superiority NOT DEMONSTRATED. Gate F NOT PASSED.**

Scientific execution HEAD: `41ca548ed065b3e6dedd50dbc42ebb1b8df5f512`.
Published log commit: `134d96995e77df0bcdd25fc046ad2b205a5c3644`.
Log SHA256: `85c1aaabd0a9d7248cf0a563fd8741a27e2dca6bc7c8a4992b37e94aefcda15d`.
Summary SHA256: `d47f17ed6a467e5203f3bf5e39e5d023cfa469320f4636ca05d13d0673b09f88`.
Local summary: `runs/c224-v5f-history-cost-audit-7d510ad2c98647bfbabeabe91de81381/summary.json`.
Validation SHA256: `5be4146f3139b761837bcbe0cad25db02c46035351e3d76b1a75a1ebd00211f2`.
Measurements SHA256: `2e09353e3899f45bb2ee3598a61e72e1602858ae446a43de306abd07acbb832a`.

## Execution validity

Published metadata, summary execution identity and registered HEAD agree. The log-publication commit
has the scientific execution as its parent. Regression2465/2465 OK (99.423s); all quality parity
checks passed; cost_audit_gate True; protected inputs preserved; tracked tree clean;
run_execution_valid True. Verdict is based on published console/metadata plus recorded local
artifact checks, not reviewer-side re-execution of the user's artifacts.

## Measured results

Uncompressed canonical audit-export bytes, not native model/checkpoint size:

| History events | H1/H2 candidate | Full-history replay | Candidate minus replay | Candidate median query ms | Replay median query ms |
|---|---:|---:|---:|---:|---:|
| 8 | 5743 | 4285 | 1458 | 0.3086 | 0.3069 |
| 32 | 11181 | 9044 | 2137 | 0.5951 | 1.2293 |
| 128 | 33100 | 28113 | 4987 | 0.5490 | 3.1948 |
| 512 | 121183 | 104657 | 16526 | 0.6936 | 8.6449 |

Candidate warm raw rereads: [0,0,0,0] bytes/query.
Replay warm raw rereads: [1579,6338,25407,101951] bytes/query.
Both arms retain identical complete raw UTF-8 evidence. All four final symbolic/provenance and
numeric-response comparisons passed the registered tolerance1e-10.

At512 events: raw101951 bytes; candidate source index15267; candidate complete bank/state export3965;
baseline bridge2706. Candidate construction/apply/commit151.5921ms and index construction2.3427ms
were recorded separately. H2 numeric W/b alone occupies48 bytes but is not the total memory cost.

Reachable-data estimates at512 events: candidate208711 bytes; replay107294 bytes. These estimates
exclude process/runtime/allocator overhead and peaks. They must not be called total application RAM.

## Interpretation

The audit succeeded, while the candidate is larger at every measured history length. At512 events
its export is approximately15.8% larger than the replay arm. Its query median is lower in this run,
but only three measured trials/arm were taken; timing is descriptive, not a statistical speed claim.

The design trades retained current state/index and construction work for avoided raw replay.
This does not yet identify a FOLD-R-specific advantage: a plain incrementally maintained symbolic
MemoryState can also avoid replaying history on every query. Comparing only against full replay is
not sufficient to attribute query savings to the response capsule.

Two live factors were held fixed. This experiment does not establish many-factor lookup scaling,
neural memory quality, compression advantage, bounded index growth, or Gate F completion.

## C225 proposed one-question intervention

Add the missing stateful comparator: retain a plain current MemoryState, update it once per event,
and evaluate it with the existing independent full-system solve. Compare it with H1/H2 using the
same raw ledger, source-index bytes, numeric bridge, history sizes, precision and query workload.

This isolates what the current H1/H2 representation adds beyond ordinary incremental state retention.
No production optimization, retraining, raw deletion, new semantic dataset or Gate F decision.
Measurement PASS remains separate from any cost-superiority claim.

C225 is not registered by this acceptance document; consult its preregistration and authoritative
handoff for execution permission.
