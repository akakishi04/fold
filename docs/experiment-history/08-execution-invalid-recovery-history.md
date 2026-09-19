# Execution-invalid and harness recovery history

## Purpose

This file records failures that were **not scientific evidence**. They matter because they explain
why multiple attempts may exist for one C-number and because they identify recurring harness risks.

Never count these attempts as VALID NEGATIVE results.

## Representative execution-invalid incidents

### C78
The first attempt had a focused unit-test bug that required gradients for route-specific parameters
not exercised by the test. It was retried under the same C-number.

### C174 repository migration
Standalone-repository migration exposed obsolete ExpectedHead/source guards. Attempts that stopped
before the scientific benchmark were treated as INVALID and repaired without changing the
scientific question.

### C186 — inherited NPZ size ceiling
Accepted C185 `episode-predictions.npz` expanded to ~67.5 MiB, exceeding an older generic 32 MiB
loader ceiling. The benchmark stopped before model/episode evidence. Recovery added a C186-specific
schema-aware reader; no threshold/model/cohort change.

### C189 — three harness failures before success
1. malformed source blob containing NUL bytes;
2. manifest SHA transcription mismatch;
3. synthetic unit-test source epoch/revision mismatch.

All were execution-invalid; the eventual successful C189 used the unchanged scientific contract.

### C190 — replay/batching and mock recovery
A completed run exceeded the preregistered <=1e-6 parent-logit replay guard because duplicate
initial observable states were evaluated in a different expanded batch context. Recovery evaluated
each unique observable state in the accepted parent ordering and memoized the output across hidden
world copies. A later retry then exposed unit-test mock call-order assumptions after memoization.
Those test mocks were corrected without changing science.

### C191 — wording-only unit-test assertion
The registered manifest correctly said post2 NEEDS had exactly one unobserved fact; one test looked
for a different phrase. Benchmark did not run. Assertion was aligned to the existing manifest.

### C192 — wrong parent artifact loader
All 1,533 tests passed, then the benchmark called C191's helper for reading **C190** predictions
instead of C192's own loader for the C191 schema. It stopped before block1 with
`C190 prediction schema drift`. Loader dispatch was corrected only.

This incident triggered the explicit **Experiment authoring quality gate**:
- parent artifact schema audit;
- loader-dispatch audit;
- runner/CLI index audit;
- call-order/resource path integration coverage;
- manifest/hash/test-count consistency;
- source-level verification before presenting a new C as runnable.

### C195 — two harness failures before success
1. synthetic reference fixture omitted the leading batch dimension;
2. benchmark guessed nonexistent C191 summary aliases (`second_provider_calls`, `final_needs`)
   instead of the actual record keys.

Both were repaired under the same C195 scientific contract.

## Recurring failure classes

1. **schema drift / wrong generation**
2. **parent helper used for the wrong parent generation**
3. **manifest/hash transcription**
4. **synthetic fixture does not match real TaskView/runtime contract**
5. **mock call-order assumptions after implementation restructuring**
6. **repository migration/source-identity guards**
7. **generic infrastructure ceiling inherited by larger artifacts**

## Process conclusion

A new C-number should not be handed to the user merely because unit tests exist. Authoring review
must verify the actual run path, parent artifact contracts and runner argument wiring.

For cleanup, historical invalid logs/recovery notes can be retained as documentation/Git history;
their broken working-tree implementations do not need to remain executable unless a current
regression explicitly depends on them.
