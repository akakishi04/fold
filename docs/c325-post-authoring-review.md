# C325 post-authoring review

Review date: 2026-10-16 (Japan time).
post_authoring_review = PASS
Review target / source-registration HEAD:
b5521f0db9e6b08789cc4567c35cc6a22d74dd2d.
Acceptance base: 6c3198793f0f6b852fa96be125323763cbfdddde.
This review authorizes activation of C325, not a scientific verdict or a claim that
native Windows/full regression/fitting already passed. Use the final activation
HEAD in the user command, not the source-only review target above.

## Independent committed-byte review

After the complete source/tests/runner/launcher/preregistration commit was published,
all six own files were fetched again at the exact target commit and reread in full.
Long Python files were retrieved in consecutive, complete line ranges. Their returned
Git blob IDs were independently compared with Git blob hashes of the local raw files
used for the following tests. Every file matches:

| File | Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c325_mixed_name_coverage.py | 86e6a4b5666d42b805c1e21b34a40acde0088709 |
| tools/c325_execution.py | 26dc2a3dcd548fd2c135a10e88ff8bcebe1578ad |
| tests_lm/test_v05_c325_mixed_name_coverage.py | 612be64f80ab0327370f7c9433c220a892b93aba |
| tools/run_c325.ps1 | c9f89e2fbbd8ea53c49eededd5b40a07c4750ae0 |
| tools/invoke_c325.ps1 | a51f3d327ab86dc7752b6dfccbaa62d00a846782 |
| docs/experiment-ledger-addendum-c325-preregistration.md | 9f9e9a924c51d5201d0f43c4547bd4a8469df7dc |

The remote compare against the acceptance base contains only those six added files
and an exact historical handoff snapshot. No accepted source, test, output, launcher,
dispatcher or scientific threshold was edited. This review and activation update
are subsequent documentation-only changes, separate from C324 acceptance.

## Reexecuted author-side checks

After the remote reread and blob matches:

- 56/56 own tests PASS, zero failures/errors/skips; 2.272 seconds.
- CP932-default-file-encoding emulation: 56/56 PASS, zero failures/errors/skips;
  2.525 seconds. This is explicit default-open emulation, not native Windows.
- All three new Python files compile/import, decode as UTF-8 and contain no NUL.
- Recursive bytecode LOAD_GLOBAL/import-binding audit: zero undefined global names.
- Manifest self-hash matches
  03ed2ba1d2d2951087c70ce41ddf39756674a30ac4cef56671e158eb80fff3d0.
- The actual own unittest loader contains exactly 56 tests. The additive suite test
  uses an explicitly synthetic 5490-test historical inventory plus the actual own
  loader, verifies total5546 and uniqueness, and rejects duplicate IDs.
- The compact console adapter processed all ten actual accepted C324 measurement
  records from the uploaded console, without model execution or scientific changes.
  Complete local cell measurements are retained by the writer; only console
  representation and unittest verbosity are smaller.

Environment: Linux Python3.13.5, PyTorch2.10.0+cpu, NumPy2.3.5, two CPU threads.
Real temporary Git repositories, file hashes/JSON, weights_only torch bundles,
erroring subprocesses, and the numerical training-loop toy fixture were exercised.
The toy's original-family one-update arithmetic exactly matches an explicit
CE/AdamW/clipping reference; changed family changes updates, and nonfinite logits stop.

Production execute_stages is exercised for normal and finite-negative completion,
failed regression before fitting, and saved-summary mismatch before finalization.
The actual controller is exercised for science-then-fresh-verify and no automatic
retry on failure. These explicit fixtures are not ten-model scientific C325 runs.

## Source-level scientific and parent-writer audit

The unchanged C324 training/evaluation/checkpoint writers, analyzer, raw schemas,
query-pair accounting, native dependency checks and replay counts were reread.
The actual inherited C315 plan_for_order/schedule_stats and C316 context were also
read: schedule length values are 2/3/4, each epoch consists of four 48-row updates,
and the existing query-pair inventory and saved logical order are retained.

C325 changes only the length-four template family in fitting. Whole length-four
epochs alternate old/interior starting old, giving every TRAIN row exactly50/50
exposures without splitting query pairs. The control uses100 interior exposures.
Length2/3, logical schedule, target, optimizer, mean_last readout, capacity, steps and
paired initialization are fixed. Fresh325001..325005/order325101..325105 are explicit.
Training receives only validated TRAIN tensors and targets, never HOLDOUT selectors.

The actual C324 heldout_contrast implementation is reused for interior contrasts.
Original2..6 contrasts adapt only profile dictionary keys, not predictions or labels.
All domain gates retain the original scorer. The all-five fixed C325 gate separately
requires candidate interior/original retention, positive original answer/pair gains
and nonnegative interior answer/pair gains. Rescue/regression count conservation is
checked both when scoring and in fresh saved-result verification. No C324 gate is
rewritten, and no failed seed can be hidden by pooling.

The immediate parent is the exact accepted C324 primary summary AND R6 envelope.
Their pinned hashes, execution identity, schemas, original scientific work, full5490
receipt, seven verifier completions/nine reuses and exact source/input unions are
checked before fitting. All1501 inherited input bytes and all802 inherited Git source
pins are checked; ten immediate-parent files and six own files extend protection to
808sources/1517inputs. Direct new code, lazy C324 dependencies, R4/R6 helpers and all
supplemental regression inputs are protected. There is no fallback to the old792 pins.

The saved C324 checkpoint tensors and evaluation records are read with weights_only,
and unchanged C324.analyze reconstructs the immediate parent's complete saved metrics.
The older C316..C322 semantic verifier bodies are NOT recursively rerun in C325;
their accepted identity and all inherited bytes remain validated. This scope is
explicit in the new contract and is not described as fresh ancestor execution.
No accepted function or module global is patched by the C325 scientific path.

All1517 input files use unchanged R4 native Windows read leases, independent first
hash checks, and final uncached rereads. The worker checks parent dictionaries remain
unchanged. All ten newly trained states undergo actual model replay, then saved child
checkpoint/evaluation files are independently reread for semantic reconstruction.
A separate process verifies the complete saved summary/envelope, exact parent/child
source and input unions and every saved output's bytes/size. Neither verifier refits.

## Launcher, logging and scope boundaries

The existing invoke_active_v2 dispatcher remains unchanged. The user command parses
that dispatcher explicitly; it parses the selected launcher, which parses itself
and run_c325.ps1 before starting Python. Branch/tracked-tree/ExpectedHead/unique ACTIVE
checks occur before scientific logging and publication. The runner uses the existing
.venv-py31315 Python and exact named CLI options; output folders are unique local runs.
Scientific status FAIL returns a valid finite outcome, not a retry request. Native
process/test/source/input/schema/replay/envelope failures stop the same C325.
Log publication uses the existing publisher, never starts science again, and records
scientific execution HEAD separately from the descendant publication commit.

No PowerShell interpreter was available on the author host, so no native AST execution
is claimed here; the mandatory user-side AST chain is retained and source-reviewed.
Native Windows read leases, authoritative Python3.13.15/PyTorch+cu130 execution,
full5546 historical regression and ten-model C325 fitting were NOT run by the author.
The registered user execution must pass native preflight and ALL5546 tests before fit.
No CI, paid service, environment reinstall, artifact deletion or automatic retry was
added. Gate F remains NOT PASSED and C326 remains NOT REGISTERED.
