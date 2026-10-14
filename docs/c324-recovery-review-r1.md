# C324 R1 post-authoring recovery review

post_authoring_review = PASS
Review target HEAD: 04e959b6164fe71981720f80fa788d26c169621d.
Failed operational invocation target: dc66a0e14f2847c2e56f387864b384645351b28b.
Scope: same-C324 preflight repair, NOT scientific execution acceptance.

## Remote source review

After committing the repair, all three changed executable/test files were fetched
again at the immutable review target. The changed classifier/callers, preflight
stages, regression cases and complete runner were reread. Returned whole-file Git
blob IDs were independently matched to the local files subsequently retested:

| Path | Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c324_interior_coverage_training.py | 2fc9e31c7037313a3fadb126af9b153608c0ac6e |
| tests_lm/test_v05_c324_interior_coverage_training.py | 21b71da7bcbbeb288b32068e8073def4a7821dcd |
| tools/run_c324.ps1 | c87abf4be0a3067fcf071635d26708141ddd2824 |

Remote comparison against the failed invocation target showed exactly these three
modified files and two added explanatory documents. No accepted ancestor, existing
launcher, dispatcher, experiment specification, checkpoint or published log changed.
This review/activation commit changes only documentation after source review.

## Executed checks

Environment: Linux Python3.13.5 / PyTorch2.10.0+cpu, isolated C324 workspace.

- Original six-file snapshot matched its immutable source blobs; own64 PASS1.618s.
- Patched own64 PASS1.570s; CP932-default-file-open emulation own64 PASS3.065s.
- After committed remote-file/blob matching: own64 PASS1.495s, zero failures/errors.
- A separate real torch.nn.Embedding probe reproduced the old sparse.py rejection
  under an enclosing nominal repository root, then passed the new guard on the
  exact same object. This used unmocked inspect.getfile and actual sysconfig paths.
- Extended tests cover12 table-driven path/namespace cases, missing configured
  paths, a pinned local dependency, direct module dispatch, actual torch classes,
  and a runtime/local mixed module graph. No existing test ID/assertion was removed.
- Existing source-level tests still pass. New runtime-class checks preserve the
  inspected model tensors and RNG. Windows-style directory layout is emulated;
  this is not a claim that Windows itself was executed.
- All four Python files and three embedded runner programs compile; symtable
  free-global/import audit passes. The unchanged own loader reports64 tests.
- AST comparison: only check_dependencies and progress statements in precheck /
  runtime_preflight differ among existing benchmark functions. One new classifier
  helper and its sysconfig import were added. All scientific functions, manifest,
  model factory, TRAIN intervention, fit, evaluators, scorers, gates, persistence
  and replay logic are unchanged.

Manifest still b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
Own64 (20+44), full5357, loaded5358, modules210, source792, protected1491, parents50.
No new exclusion, lowered gate, new seed, resumed training or result replacement.

## Guard and execution boundaries

An unpinned repository source is not ignored merely because its path contains
.venv/site-packages. Installed runtime classification needs BOTH the torch/numpy
namespace and location below the active interpreter's sysconfig purelib/platlib
package directory. Local torch shadows and FOLD classes remain subject to pins.
Third-party package byte authentication is outside this repository-source guard;
this repair does not claim that it authenticates the installed environment.

No PowerShell executable was available here. The only runner changes are two
Write-Output lines. The mandatory dispatcher -> launcher -> runner ParseFile
execution path is unchanged, as are50 parent arguments and postcheck argc53.
The full5357 suite and50 real Windows parent archives were NOT run here. They
remain required in the retry before scientific fitting. No speedup is claimed.

## Decision

The observed false rejection is repaired with regression coverage, with the
scientific specification unchanged. Same-C324 retry may be issued at the final
review-record HEAD after a guarded fast-forward of feat/sft-target-loss. Preserve
the initial skipped invocation as operational history, not a scientific negative.
