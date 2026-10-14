# C324 recovery R1 — installed runtime package is not repository source

## Status and evidence boundary

Retry the SAME C324. This is an operational preflight failure, NOT an accepted
scientific negative and NOT a completed scientific execution. Formal state remains
C324 ACTIVE / NOT YET JUDGED; C325 NOT REGISTERED; Gate F NOT PASSED.
Failed invocation target: dc66a0e14f2847c2e56f387864b384645351b28b.
The user reported the traceback below after the long launcher/preflight interval.
The launcher returned experiment_executed=False and did not attempt publication.
There is no new scientific execution HEAD or published scientific log commit to
invent for this skipped invocation. Preserve the local preflight log; the unchanged
launcher archives an existing c324-preflight-last.log before another attempt.

```text
File "<string>", line 8, in <module>
    b.runtime_preflight(paths, Path.cwd())
File "M:\asobiba\fold\fold_lm\v05_benchmarks\model_c324_interior_coverage_training.py", line 675, in runtime_preflight
    check_dependencies(Path(root).resolve(),pins,cx,model)
File "M:\asobiba\fold\fold_lm\v05_benchmarks\model_c324_interior_coverage_training.py", line 204, in check_dependencies
    require(Path(filename).resolve().relative_to(root).as_posix() in pins, 'unprotected model class:' + filename)
ValueError: unprotected model class:M:\asobiba\fold\.venv-py31315\Lib\site-packages\torch\nn\modules\sparse.py
invocation_skipped = AUTHORING_RUNTIME_PREFLIGHT_FAILED
detail = C324 parent/TRAIN/native-gradient precheck failed
experiment_executed = False
execution_log_publish_attempted = False
```

This traceback is a user-provided excerpt, not a separately hashed full log.
Control flow reached the first preflight model dependency check after parent
precheck and TRAIN table/schedule preparation. It stopped before the native
forward/backward probe, own-test process, full-regression process or scientific fit.
No C324 learning, model-capability conclusion or accepted output follows from it.

## Minimal cause and repair

The old check identified any inspect.getfile(model_class) below the repository
root as repository-owned source. In the user's layout the active virtualenv is
below that root, so torch.nn.Embedding's installed sparse.py was incorrectly
required in the Git source pin map. This is a checker ownership-classification
bug, not evidence that PyTorch was missing or needed reinstalling.

check_dependency_file now applies the same ownership rule to direct modules and
model classes. An already-pinned local source still follows the existing blob and
byte protection. Only torch/numpy namespaces under this running interpreter's
sysconfig purelib/platlib package directories are classified as installed runtime
dependencies. Merely containing .venv or site-packages in a filename is not enough.
Unpinned FOLD source, namespace mismatches, unrelated virtualenvs, local torch
shadows, directory-prefix lookalikes and path traversal remain rejected.
No global monkey-patch, pin-waiver switch, ignored repository namespace or
site-packages-wide exclusion was added. This distinguishes dependency ownership;
it does NOT claim to authenticate every byte of the third-party installation.

Existing C324 tests 09 and 15 were extended with runtime/local-boundary subcases,
a real torch Embedding/Linear inspection and a mixed runtime/FOLD-class graph.
Test 43 additionally checks early progress placement. No existing assertion/test
ID was removed. Own64=component20+benchmark44; full5357 and the exact inherited
single C204 exclusion stay fixed. The manifest SHA is unchanged:
b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.

Source pins792/protected inputs1491, all50 parent hashes, all8 OWN paths, seeds,
model initialization, optimizer, training schedule, 1200 steps/model, task views,
scorers, gates, scientific workload, checkpoint replay and artifact schemas stay
unchanged. An AST comparison confirms only check_dependencies, precheck progress,
and runtime_preflight progress changed among existing functions. The new helper is
inside the already-OWN benchmark file, not an unprotected new module.

## Author-side checks already executed before committing

Linux / Python3.13.5 / PyTorch2.10.0+cpu, isolated six-file C324 workspace.
The six original source/test/runner/launcher files were reconstructed from the
immutable GitHub contents and independently matched to their original Git blobs
before edits. Original own64 passed (1.618s). Patched own64 passed (1.570s), and a
separate CP932-default text-file-open emulation passed own64 (3.065s).
An explicit red/green probe used actual torch.nn.Embedding and unmocked inspect:
the old guard rejected installed sparse.py when the nominal repository enclosed
the installation; the new guard accepted the same unchanged object. Windows-style
nested virtualenv paths are also tested through configured-path emulation.
Four Python files and three runner Python here-strings compile; free-global/import
binding audit is clean. The actual own loader still counts64 unique tests.

These are software tests, NOT Windows execution, a real50-ancestor archive check,
a full5357 run or C324 scientific evidence. A post-commit remote-byte review must
be recorded separately before publishing a retry HEAD. Actual PowerShell parsing
remains in the unchanged dispatcher/launcher path; PowerShell was unavailable in
the authoring container. The runner change only adds two Write-Output lines.

## Latency note

Early stage markers now precede the expensive parent check and identify completion
of parent verification, source/input checks and TRAIN preparation. This is improved
observability, not a demonstrated startup speedup. No ancestor verification cache,
regression skip or scientific-work reduction is enabled by this repair.
See experiment-preflight-latency-followup.md for the separately scoped request to
reduce startup overhead beginning with C325 or a later authorized harness update.
