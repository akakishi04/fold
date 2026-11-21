# C225 acceptance and C226 boundary

## Formal verdict

**C225 ACCEPTED PASS as a measurement audit. No efficiency superiority established.**
Gate E remains PASSED; Gate F remains NOT PASSED.

Scientific execution HEAD: `6669add6de53247e60731a3f23e7bed9350deec3`.
Published log commit: `88395cb0d44b0ca02fcb106967b97d966dcbe1b3`.
Log SHA256: `f1d1bf677a49cabbb3974fce6e7077c051018335736f1a620d95034b95d57005`.
Summary SHA256: `b54943514cebb06161851e6a79c9eb4e8fd6766429f6f2e0e2f34c79c52a78ad`.
Local summary:
`runs/c225-v5f-stateful-baseline-4df0cd59e7c34942a3d33b0932863b0f/summary.json`.
Validation SHA: `94e2028aaaff24f9cc03480abde49c2e41674d833141745e6bc34f9852620a29`.
Measurements SHA: `50e82a0a655ab63ddf00da04edab1995c7b99064ae493ba5320a0d2f348362a2`.

## Execution validity

Published metadata identifies the registered execution HEAD, and the log-publication commit has
that HEAD as its parent. The console reports 2497 focused tests in64.911 seconds, OK; prechecks
and artifact postchecks passed, inputs preserved, tracked tree clean, run_execution_valid True.
All four measurement points passed full current-state/provenance and numeric quality parity.
The original C224 candidate export inventories were preserved exactly.

This acceptance uses published console/metadata and the recorded local artifact checks. It is not a
reviewer-side rerun of local-only user artifacts or a claim to have copied those artifacts.

## Deciding measurements

| History events | H1/H2 export B | Stateful symbolic export B | H1/H2 query median ms | Stateful symbolic query median ms | H1/H2 / symbolic |
|---|---:|---:|---:|---:|---:|
| 8 | 5743 | 5328 | 0.3271 | 0.2727 | 1.1995 |
| 32 | 11181 | 10764 | 0.2232 | 0.1201 | 1.8585 |
| 128 | 33100 | 32681 | 0.1720 | 0.0877 | 1.9612 |
| 512 | 121183 | 120764 | 0.1789 | 0.0865 | 2.0682 |

Candidate extra export bytes:415,417,419,419. No size favors H1/H2 storage.
Both arms reread zero raw bytes/events per warm query. The shared raw and source-index bytes match.

At512 history events, construction was81.947 ms for H1/H2 versus5.0717 ms for symbolic state;
shared index construction1.7243 ms. Reachable-data estimates were208711 versus207651 bytes.
The symbolic arm shares the complete numeric bridge, including an unused compiled capsule.
It is not presented as an independently minimized implementation.

## Interpretation

On this two-live-factor, two-dimensional numerical reference, H1/H2 used more retained bytes and
had slower descriptive query medians at every measured size. A PASS means the registered measurement
and correctness checks succeeded, not that the representation won.

C224's avoided full-history replay is not a capsule-specific benefit: ordinary retained current
MemoryState also avoids replay. The C225 measurements now demonstrate that distinction directly.

Query timings are three measured trials after one warmup. They are descriptive, not a statistically
established speed ratio or general conclusion about every workload. Export bytes are canonical
uncompressed audit files, not native checkpoint sizes. Reachable-data estimates are not process
RAM/VRAM peaks. Only two current factors and a2x2 full numerical system were measured.

## Next one-question boundary (not registration)

A2x2 full system with update rank2 has no dimensional reduction. Before changing production code,
measure the same H1/H2 versus stateful full-solve paths while varying only full-system dimension,
keeping two observed factors, two readout coordinates and update rank2 fixed.

The proposed C226 family should preserve the C225 n=2 anchor and couple additional hidden coordinates
to the visible coordinates rather than append irrelevant disconnected padding. Count the entire
retained bridge, raw evidence, index, state and setup work. Keep check=True and all safety checks.
Report positive or negative cost outcomes without moving a speed/storage gate after observation.

This is a conditional numerical-dimension study, not many-factor scaling, natural-language inference,
production optimization or Gate F completion. C226 is not registered by this acceptance document.
