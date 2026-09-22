# C228 acceptance and C229 boundary

## Formal verdict

**C228 ACCEPTED PASS (measurement audit). Gate F NOT PASSED.**
There is no measured update-plus-query speed advantage for the current H1/H2 path in this workload.

Scientific execution HEAD: `0b78d33987d0e123efff58675693c4f19b81953e`.
Published log commit: `68cba193bb1affe648f522f41ce6444f8c39e168`.
Console log SHA256: `9ca6822e5c36b02d2129398aa1bec7b130b2fb00d82a83371a2f27b30d51fd91`.
Summary SHA256: `44ddf79b6ae1aadb5fb28e37e8528e40c1384b13a152283badbb9eb1be20e9a6`.
Local summary: `runs/c228-v5f-update-query-76eea62720cf4857a7122cd48c400f1a/summary.json`.
Validation artifact SHA256: `29779710b3826659244ea89f3c57f8dffdc0b824fe0247a205150b63ce8f617b`.
Measurements SHA256: `36bf474db858daf9ccb6a01f5b13d4980edf1dda904c5d9c7bfa124501eb1aab`.
Quality checks SHA256: `e4e58785965cd19554dc8680fa0e3e433498f8048df44daad19130c72f415f10`.
Exports ZIP SHA256: `54cd9ac63fe598765b5a49d4b374f2350361f44c797e129d7dff2c2cf70bff28`.

## Execution validity

Published log reports 2593 tests in82.134 seconds, OK; all12 cells present; all_quality_parity True;
initial_parent_parity True; update_query_audit_gate True; protected inputs preserved, tracked tree
clean and run_execution_valid True. Execution-to-publication Git comparison contains only the
C228 console log and receipt. Acceptance uses this recorded local artifact verification, not a
reviewer-side rerun of user-local artifacts. New science and publication HEADs remain distinct.

## Deciding results

The following ratios are H1/H2 median stream time divided by checked-factor/rhs-refresh median
stream time. Stream time includes12 updates and the registered questions after each update; setup
and export are separate. Values greater than1 mean the current H1/H2 path took longer.

| Numerical dimension | 1 query/update | 4 queries/update | 16 queries/update |
|---|---:|---:|---:|
| 2 | 2.9388703149744853 | 4.093452170843628 | 5.3712832 |
| 16 | 2.8493098688750864 | 3.449638940893287 | 4.5253708339719685 |
| 64 | 2.7943794163654996 | 4.173241360700251 | 4.553497845763727 |
| 256 | 1.589998581176076 | 1.903756697262948 | 2.1844487984849392 |

All12 are unfavorable to H1/H2, spanning about1.59x to5.37x the comparator time. Correct current
answers/state/provenance were preserved, including after each replacement; the audit gate did not
require favorable timing. Do not present this PASS as a performance win.

## Interpretation and confounds

C227's frozen-state speed loss persists when bias-only updates are included. The competitor is
allowed to retain its valid full factor and refresh rhs/state binding instead of refactorizing
needlessly. There is no evidence here that updates rescue the current H1/H2 implementation's speed.

This is not a proof against every reduced-memory architecture. It is a narrow comparison of the
current implementations with two live factors, fixed2-port/readout interface, matrix-invariant
bias changes, four dimensions and three descriptive timing trials. There is no matrix-changing,
natural-language, many-factor, answer-cache or peak-process-memory conclusion.

Earlier query traces showed repeated checked small solves on the H1/H2 side versus checked-factor
reuse on the comparator. Those traces alone do not quantify where the time goes. Do not attribute
all observed loss to validation, Python overhead or numerical kernels without profiling.

## Next one-question boundary

C229 will profile the same C228 update/query workload without optimizing or changing either arm.
Question: which actual function calls account for the current candidate update/query work, and is
the observed cost concentrated in numerical kernels or in the surrounding state/validation work?

Collect function call counts plus inclusive/self times for separate update/query phases; do not
sum nested inclusive times or mistake profiler-perturbed timings for fresh speed evidence.
Require exact C228 final-export identity and identical answers/state/provenance with profiling off
and on. No safety checks are removed. This diagnostic is not a search for a new favorable workload.

C229 is NOT REGISTERED by this acceptance document. Register it separately after authoring.
