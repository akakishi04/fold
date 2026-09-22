# C229 preregistration — unchanged-workload function attribution

**C228 ACCEPTED PASS. C229 ACTIVE / NOT YET JUDGED. C230 NOT REGISTERED.**
Gate E PASSED; Gate F NOT PASSED.

## One question

Which actual functions account for the current H1/H2 update/query work on the same C228 workload?
Measure call counts and function self/cumulative times before changing the implementation.

Changed condition: add scoped cProfile observation with an unprofiled correctness control. No
production optimization, alternate workload, new data, neural training or weakened comparator.

## Parent evidence

Scientific HEAD: `0b78d33987d0e123efff58675693c4f19b81953e`.
Published log commit: `68cba193bb1affe648f522f41ce6444f8c39e168`.
Summary SHA: `44ddf79b6ae1aadb5fb28e37e8528e40c1384b13a152283badbb9eb1be20e9a6`.
Validation SHA: `29779710b3826659244ea89f3c57f8dffdc0b824fe0247a205150b63ce8f617b`.
Measurements SHA: `36bf474db858daf9ccb6a01f5b13d4980edf1dda904c5d9c7bfa124501eb1aab`.
Local summary:
`runs/c228-v5f-update-query-76eea62720cf4857a7122cd48c400f1a/summary.json`.

Read the accepted parent summary, all208 source pins,280 inherited protected inputs and five
artifacts. The child adapter validates the actual ordered12-cell measurements with parent.row_gate
and is called by both precheck and run. Required parent fields include numeric_dimension,
queries_per_update, retained_inventory and stream_ratio_h1h2_over_cached. The last field is
historical uninstrumented context, not newly measured by the profiler.

## Fixed workload and scope

Dimensions2/16/64/256; queries per update1/4/16;32 initial events;12 bias-only beta replacements;
two live factors; update rank/readout2. Reuse C228 ledger_parts and the C226 matrix factory unchanged.
CPU threads2, deterministic algorithms, float64 numeric path, tolerance1e-10.

For each of12 cells run one unprofiled control trajectory, then one profiled trajectory, with
identical update order and alternating arm order by update. No randomized/statistical timing claim.
The candidate uses original apply/commit/read. The comparator uses original symbolic mutation,
checked factor/rhs refresh and query_cached. No final-answer cache or source monkey patch.

## Recorded phases

candidate_update, candidate_query, cached_update, cached_query each have separate cProfile objects.
Each phase is entered12 times; each query phase contains12*q actual query calls. Record complete
function identities, total/primitive counts, self time and cumulative time. Export all records and
top10 self-time functions per phase. Do not sum overlapping cumulative times.

Exclude setup, correctness oracle, audit snapshots, report construction and serialization from
recorded phases. Report boundary wall times with and without profiling for instrumentation context
only. Profiler overhead is not subtracted and these times must not be cited as a new speed win.

## Fixed gate

All12 cells, ordered by dimension then burst, must have:
- off/on query results matching current full_reference within1e-10;
- full symbolic-state/provenance parity after all12 updates;
- same checked factor retained, complete evidence/index retention;
- off/on final export inventories exactly equal accepted C228 retained_inventory;
- no query state mutation;
- valid nonnegative profile records with primitive<=total calls and self<=cumulative time;
- exact candidate apply12/read12*q and cached refresh12/query12*q function counts;
- all four phase invocation counts12;
- external profiler never overwritten and hook restored after each call;
- no new training and no accepted source changes.

PASS does not require favorable costs or any predetermined bottleneck. Complete diagnostic/parity
failure is scientific FAIL. Source/artifact/schema/regression or incomplete execution is INVALID /
RETRY SAME C229. Gate F remains NOT PASSED.

## Authoring registration

OWN6:
- `fold_lm/v05_benchmarks/gate_f_c229_cost_profile.py`
- `tests_lm/test_v05_c229_cost_profile.py`
- `tools/run_c229.ps1`
- `tools/invoke_c229.ps1`
- this preregistration
- `docs/v5f-update-query-function-profile-v0.1.md`

Source pins214. Protected inputs292 = inherited280 + parent summary/artifacts6 + OWN6.
Direct deciding dependencies27 = previous26 plus C228 benchmark. All must be parent/OWN pinned.
Artifacts5: profile-plan, measurements, function-profiles, quality-checks, validation-summary.
No generated scientific artifacts or profiler binaries are committed outside standard console logs.

New tests32; modules114; loaded2626 /focused2625. Only inherited exact exclusion:
`tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state`.

Manifest SHA:
`3f9ce8c054db73843455447d6dc74426be570e50857cc220a3927f8777bd3723`.

## Post-authoring review

`post_authoring_review = PENDING`

Before remote review30 targeted tests passed (0.933 seconds),32 methods enumerated and manifest
matched. Executed tests include real cProfile/torch solve invocation counts, callback semantics,
exception/hook restoration, external-profiler protection, nested self/cumulative accounting,
mutation absence, parent adapter and profile-cell negative controls, and a synthetic12-cell run
covering loader/output/postcheck order. Synthetic fixtures are not the accepted memory backend.

Not executed in the authoring container: test31 actual parent trajectory/export/profile counts,
test32/full2625 historical suite, Windows PowerShell AST parsing, user-local artifact precheck or
formal C229 profiling. Clone failed DNS resolution. Do not represent the targeted tests as those
missing execution checks.

Before giving an execution command, re-fetch committed code/test/runner/launcher, match full blob
identities against the tested copies, rerun targeted tests, review real parent method/field meanings,
profiling boundaries and count identifiers,214/292 accounting,27 dependencies, CLI indices and
complete launcher guards. Record the review HEAD and its limitations. The runner executes32 own
tests, then2625 focused tests, then profiling. Failures stop before the next phase and publish logs.

## Stop

Use invoke_active.ps1 with the final reviewed HEAD. Judge C229 before C230.
No cleanup, history rewrite, new CI, unrelated architecture or Actions-storage changes.
No performance/peak-memory/LLM-reasoning/Gate F claim from function-profile timing.
