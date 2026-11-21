# C324 post-authoring review

post_authoring_review = PASS
Review target HEAD: 926659460e7d93207122e8d19e5b26bb3f578ac8.
Acceptance base: 88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf.
Review date: 2026-10-14.
Scope: complete C324 authoring package, not a C324 scientific verdict.

## Committed remote-byte review

After completing and committing source/tests/runner/launcher/preregistration/design,
all eight OWN files were fetched again from the immutable target HEAD and reread.
Large Python files were retrieved in consecutive source ranges, including their
entry points. The returned Git blob IDs match independently computed local raw-byte
Git blobs for every file; no scientific source was changed during this review.

| Path | Verified Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c324_interior_coverage_training.py | e60afd2ba82a59d3aaa9b440276b1f5ca3e2521e |
| fold_lm/v05_benchmarks/c324_training_templates.py | 16d77bdc65971eb3cddf054da778096619b2eed9 |
| tests_lm/test_v05_c324_interior_coverage_training.py | e577846ce7f263f07f53e5a13a2c9a89e02c5cf1 |
| tests_lm/test_v05_c324_training_templates.py | bd74d754560745932847a674ac974f57df45e13c |
| tools/run_c324.ps1 | a6c3b7cbfe30c50baae6d1787a0c7d90c9488295 |
| tools/invoke_c324.ps1 | cc92a0e6efe8c4b203a1d81a03faa45f9725fea0 |
| docs/experiment-ledger-addendum-c324-preregistration.md | bb8eb90c22d1fbdede5cd39ca85358850823411c |
| docs/v5b-interior-coverage-training-v0.1.md | 2212c12500ddd135b3618a125e9de4ed8e14619c |

Manifest self-hash:
b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f.
All eight files decode as UTF-8 without literal NUL. The four Python files parse
and compile. A symtable-based free-global binding audit found no unbound names;
interpreter-provided module globals were accounted for explicitly. All three
runner Python here-strings compile. Source-string assertions were checked against
the actual function named in each test, rather than a caller's or comment's text.

## Tests actually executed after remote-byte matching

Environment: Linux / Python3.13.5 / PyTorch2.10.0+cpu, isolated C324 workspace.

`python -m unittest tests_lm.test_v05_c324_training_templates tests_lm.test_v05_c324_interior_coverage_training -v`

64 tests ran, failures0/errors0, 1.075 seconds, exit0.
A separate run with default text opens through builtins.open/io.open explicitly
emulated as CP932 also ran all64 tests, failures0/errors0, 1.213 seconds, exit0.
This is a default-file-encoding compatibility probe, not execution on Windows.

Tests include actual temporary-file hashing/protection checks, the real C324
writer and verifier with explicitly mocked model/parent dependencies, checkpoint
safe loading and tamper rejection even after descriptor resealing, no-overwrite,
exact main/CLI dispatch, paired error accounting and fixed-gate controls.
The fit arithmetic test performs two actual PyTorch/AdamW updates on a tiny
software-only network and matches an independent explicit reference exactly.
These tiny-model results are NOT FOLD capability results or formal C324 training.

## Parent writer, dependency and call-order audit

Read accepted C323 source and runner, C319 trainer/writer/verifier, C321 renderer/
scorer, C315 schedule/evaluation, C316 context, C304 readout/scorer, and C267/C270
canonical data and local-gate implementations. In particular:

- C323 produces four JSON diagnostic artifacts; it is not a checkpoint archive.
- All50 ordered summary hashes are checked before C323.verify_artifacts is called.
- C319 is index4 of C323..C274. Its dataset.json/length-datasets.json are read only
  after recursive parent verification and independently checked against DATA_SHA /
  PROMPTS_SHA. C321.check_prompts retains canonical rendering and vocabulary bounds.
- The TRAIN selector changes only length-four strings. Both models use native
  mean_last through the original C319 policy context during fit/evaluation/replay.
- Paired fresh seeds and schedules are fixed before outcomes. Fit receives TRAIN
  tensor tables and teacher targets only; no HOLDOUT-driven selection or stopping.
- run calls the child load_bundle before all10 replays. Replay verifies tensor
  shape/dtype/digest, full fingerprint, numerical logits and exact full256 argmax.
- verify_artifacts reconstructs every JSON and summary from saved logits under
  no_neural; it neither retrains nor treats a finite gate FAIL as an invalid run.
- All784 parent pins/1478 protected inputs are retained. Eight OWN files and five
  C323 output files extend protection to792/1491. Direct helper modules and actual
  repository-local model classes are checked; the new template helper is included.

## Workload, regression and execution-path audit

Ten models;1200 updates/model;12000 updates total;576000 training row presentations.
Per model:training1200 calls plus evaluation171 plus replay171. The unchanged
original evaluator contributes144 calls/13824 rows; the interior evaluator adds
27 calls/2592 rows. Totals15420 model calls,904320 rows,61680 core calls.
Old length1 remains descriptive; original2..6 and interior local/masked/both-order
gates plus both strict paired HOLDOUT gains are required in all five seed pairs.

The actual loader for the two OWN test modules contains20+44=64 tests. Tests of
the regression extension construct the actual child suite/filter with synthetic
parent test IDs to verify ordering, unique counts and the sole inherited exclusion.
The expected real full suite is the accepted C3235293 plus64=5357 tests across210
modules;5358 loaded minus the exact inherited C204 exclusion. The real full-repo
suite was NOT imported or run in the isolated author workspace. The runner MUST
construct it, validate actual IDs/counts, and run the full ordered one-process suite
before scientific execution. No additional exclusions or parent test edits.

The50 launcher paths were compared with the accepted C323 launcher:prepend the
accepted C323 summary, retain the49 ancestor paths and order. Runner postcheck is
output_dir,expected_head,50 summaries;sys.argv length53,parents start at index3.
Validate/Execute arguments, module paths and C324 log publication were reread.
The scientific entry calls b.main directly rather than reexecuting an imported
module via runpy. Stale branch/tree/HEAD/ACTIVE checks precede logging/publication.
The existing invoke_active_v2.ps1 is unchanged, parses the selected launcher, and
the launcher parses run_c324.ps1; the user block parses the dispatcher itself.
PowerShell is not installed in this author workspace, so a local PowerShell AST
execution is NOT claimed. ParseFile is a mandatory part of the Windows launch path.

## Explicit remaining runtime gates

This authoring PASS does NOT claim that the user's50 local archives, actual Windows
source-file hashes, real FOLD native-gradient probe, full5357 regression, Windows
memory-counter call, scientific training or checkpoint replay already passed.
Those are mandatory runtime gates. Parent/source/finite/replay failures stop C324;
repair SAME C324 without changing the registered scientific comparison.
A finite, integrity-valid failure of the fixed capability gate is a valid negative.
C325 remains unregistered until the formal C324 verdict. Gate F is NOT PASSED.

The activation commit may change only control documentation after this review;
all eight reviewed OWN Git blobs must remain identical. No accepted source/test/
log/preregistration, protected dispatcher or CI configuration was changed.
