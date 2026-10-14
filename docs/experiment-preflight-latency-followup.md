# Experiment preflight latency — follow-up requested during C324

User request (2026-10-14): after launcher=.../invoke_c324.ps1, the startup interval
is excessively long; reduce it beginning with C325. The subsequent traceback
identified a C324 preflight ownership bug, fixed separately in recovery R1.
This document records the latency requirement; it does not register C325, change
C324 science, authorize background execution or declare a measured speedup.

## Evidence and what is not yet measured

At dc66a0e14f2847c2e56f387864b384645351b28b:
- run_c324 Validate calls runtime_preflight before own64 and full5357.
- C324.precheck calls the recursive parent loader before its first registration
  print; then checks784 inherited source blobs using one git subprocess per path.
- C323.load_parent calls C322.verify_artifacts and later C322.load_parent. The
  verifier also calls its own load_parent, so ancestor work is repeated.
- C324 Validate, scientific-run precheck and saved-result postcheck have distinct
  verification boundaries. Eliminating a boundary is not equivalent to removing
  duplicate work inside one boundary.
- The accepted C323 log records5293 regression tests in1214.580s. This is NOT a
  timing of C324's initial silent phase. The user's traceback stopped before the
  C324 own/full-regression phases, so those cannot explain that specific interval.

Exact C324 wall-clock attribution, repeated ancestor-call counts and byte reread
volume were not measured here. Avoid claiming a dominant percentage, exponential
runtime, a target duration or a guaranteed reduction from source inspection alone.

## Priority for next harness authoring

1. Add flushed BEGIN/END markers and monotonic timings for imports, parent checks,
   source pins, protected-file hashes, TRAIN probes, own tests and full regression.
   Report progress/heartbeat during long phases and preserve full diagnostic logs.
   The recovery already adds coarse early C324 markers, not a fine profiler.
2. Replace per-file Git source lookups with one exact, NUL-delimited tracked-tree
   inventory bound to the execution HEAD. Check every required path/blob without
   changing protection cardinality or conflating Git blobs with working-tree bytes.
3. Measure and deduplicate repeated ancestor verification within one explicitly
   bounded validation session. A completed result may be reused only with an exact
   source/validator identity, argument/parent order and immutable input snapshot.
   Never use timestamps alone, never cache a failure as success, never disable the
   validators and never leak mutable shared result objects to callers. Preserve
   independent pre/post mutation checks; changed or incomplete snapshots fail closed.
4. Keep the complete ordered historical regression suite. Test partition caching,
   fixture parallelism and reuse of previous-C successes are NOT authorized by this
   request. They need a separate equivalence/invalidation design and review.

## Acceptance criteria for any optimized implementation

All accepted ancestors/tests/dispatchers remain unmodified; new deciding-path helper
modules must be pinned. Compare reference and candidate valid results plus corrupt
bytes, missing files, source changes, altered arguments, namespace/layout changes,
failed/interrupted validation and mutated return-value controls. Preserve exact
failure behavior and required test ID coverage. Report measured time, calls and
bytes before/after on the SAME fixed inputs, including cache setup cost.

Do not consume a new scientific C number solely by declaring the harness faster.
C325's scientific question remains contingent on the formal C324 result. If a safe
optimization is not yet verified at registration, state the remaining latency and
retain the reference path rather than weakening integrity to claim completion.
