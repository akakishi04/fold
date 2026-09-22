# V5-F update/query function profile v0.1

## Purpose

C228 correctly measured the current H1/H2 path as slower in all12 bias-update/query cells than a
checked full-factor/rhs-refresh comparator. C229 does not search for another favorable workload or
remove safety checks. It diagnoses the current implementation before any optimization proposal.

One question: which actual functions consume the candidate's update/query work, and is the cost
concentrated in numerical kernels or surrounding state construction/validation/bookkeeping?

## Held constant

Use the same dimensions2/16/64/256, queries per update1/4/16,32-event initial prefix,12 additional
beta replacements, two live factors and2-port/readout interface as C228. Reuse the actual accepted
memory, capsule, checked factor and rhs-refresh helpers. No production source, learned weights,
regression tests, numeric safety checks or original data are changed.

Both arms retain the complete evidence/index/current state/bridge, and the cached arm retains its
factor/rhs/W guard. Require final file inventories, including cache export, to equal accepted C228
for every cell. This is byte-level parity of the comparison exports, not a new compression claim.

## Instrumentation boundary

There are four independent cProfile accumulators per profiled trajectory:

- candidate_update: evidence/index append, MemoryOp application and commit;
- candidate_query: the registered batch of current bank reads;
- cached_update: evidence/index append, symbolic MemoryOp application and checked rhs refresh;
- cached_query: the registered batch of current checked-factor solves.

Each accumulator is entered12 times. Each query accumulator contains12*q actual read/solve calls.
The profiler executes the original callable and records builtins and nested Python calls. There
are no module monkey patches, fake results, disabled checks or cached final answers. An existing
external profiler is rejected rather than overwritten; normal and exceptional completion must
restore the hook.

Setup, correctness oracle, audit snapshots, report creation and serialization happen outside the
four recorded regions. They are not assigned to a serving phase. This experiment diagnoses stream
phases, not cold setup or total application latency. C228 remains the original uninstrumented
three-trial cost comparison.

## Control and profiled runs

Each cell is rebuilt twice, first with profiling disabled and then enabled. Both trajectories use
the identical update sequence and alternate arm order by update. Every query result is checked
against the current full_reference with tolerance1e-10. Every update checks complete symbolic-state
and provenance parity and retention of the same checked full factor. Query calls must not mutate
state. Both final inventories must equal each other and accepted C228.

The two mode runs are controls for instrumentation correctness, not paired performance estimates.
They are not randomized repeated timing trials. Do not use their wall-time ratio as a new speed
claim or subtract it as a universal profiler-overhead correction.

## Function reporting

For every recorded function retain file, line, qualified function name, total/primitive call counts,
self time and cumulative time. Keep full records in function-profiles.json, and top10 by self time
for each phase in measurements.json. File/name matching is used to verify exactly:

- ChunkedMemoryBank.apply:12 candidate-update calls;
- ChunkedMemoryBank.read:12*q candidate-query calls;
- C228 refresh:12 cached-update calls;
- C227 query_cached:12*q cached-query calls.

Self time excludes child calls and can be ranked without counting nested work twice. Cumulative
time helps interpret a parent call but must not be summed with its children as separate cost.
Profiler/runtime overhead is not subtracted. cProfile's current-thread native-call boundaries do
not expose detailed internal BLAS worker activity or GPU kernel execution. Times are descriptive,
profiler-perturbed attribution signals, not exact removable overhead or guaranteed savings.

Do not pre-classify all Python work as waste, or assume repeated validation is unnecessary. The
profile should identify candidate functions for a later, separately gated design decision.

## Quality gate

Require all12 cells, exact parent inventories in both modes, all current answers/state/provenance
checks, profile record schema consistency, exact phase/read/update counts and hook restoration.
There is no timing-superiority threshold, required dominant function, or target savings percentage.
A complete parity/count diagnostic failure is FAIL. Broken source/artifacts/schema or incomplete
execution is INVALID. No next optimization is adopted merely because its theoretical opportunity
appears in the profile.

## Outputs and limits

Five local-only artifacts: profile-plan.json, measurements.json, function-profiles.json,
quality-checks.json, validation-summary.json. No snapshots, profiler binary or checkpoints go to Git.
Only the standard console log/receipt is published for the experiment.

No training, production optimization, matrix-changing relations, many-factor scaling, language
benchmark, acquisition, peak RAM/VRAM measurement or Gate F completion is claimed. Judge C229
before registering C230.
