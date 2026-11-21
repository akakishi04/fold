# C192 execution recovery

## First invalid attempt — wrong parent prediction loader dispatch

Execution HEAD: `0c83f43c85dd535deb3fcccc2310a8e3d215f3a4`
Published log commit: `e2a136ee81d861ea81b48d12697891ff42aca3a0`
Log SHA256: `03d3ce1ddc01520ddc3876be7c9ce12a1ee4bd950386ca385bc651e608b85687`.

Precheck passed and all **1533/1533** focused tests passed. Benchmark then stopped before
the first block with:

`ValueError: C190 prediction schema drift`

Root cause:
C192 defines its own loader for the C191 `episode-predictions.npz` schema, but the run path
mistakenly called `c191.load_parent_predictions()`, which is intentionally the C191 helper
for reading its **C190 parent** artifact. The function therefore expected the C190 schema and
correctly rejected the C191 output.

Recovery:
- change only the C192 run dispatch to call C192's own `load_parent_predictions()`;
- strengthen an existing C192 unit test to assert the run path uses the child loader and does
  not call the parent's parent-loader helper;
- no scientific question, manifest, threshold, cohort, seed, checkpoint, source, gate,
  workload, or interpretation changes.

C192 remains **ACTIVE / NOT YET JUDGED**. Retry SAME C192. C193 remains unregistered.

## Process-quality response

Recent INVALID frequency is too high for harness-authoring quality. The conversation protocol
and AGENTS rules now include an explicit **Experiment authoring quality gate** requiring:
parent artifact schema audit, loader-dispatch audit, runner/CLI index audit, call-order/resource
path integration coverage, manifest/hash/test-count consistency, and source-level verification
before a new C is presented as runnable.
