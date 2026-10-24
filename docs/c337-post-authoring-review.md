# C337 post-authoring review

Date: 2026-10-24 Japan time.
post_authoring_review = PASS
Source/preregistration review target: 65823e67e8973cd37681a284d5ddc5002045de9e.
Acceptance base: 5f7e434ca76132057036155c7467a15caee91b6c.
The source commit already existed when this completion review began. This review
finishes the previously missing approval and activation; it does not claim a second
implementation or a new scientific result. The activation commit is documentation
only. Use that final commit, not this source-only target, in the user command.

## Exact committed-source reread

All six own files were fetched at the exact target and read through EOF. Long
executor/test responses were read in consecutive ranges, with an overlapping final
range to recover the truncated executor ending. Locally reconstructed raw files
match the returned Git blob IDs byte for byte:

| File | Git blob |
|---|---|
| fold_lm/v05_benchmarks/model_c337_saved_value_support.py | e9f9249fdad6114d4943a6ee0aa1d0cd66a08227 |
| tools/c337_execution.py | 5ac766d9721b1a563fa137fbdd40625b0e4117b6 |
| tests_lm/test_v05_c337_saved_value_support.py | b2618bf11be9ca73697f9f6b75983c588c3f2291 |
| tools/run_c337.ps1 | 0fbb29aca81c4bc7093fc38828f8be1d398a4476 |
| tools/invoke_c337.ps1 | e85b0db25f8b7ec33ed195cca855f3414576f1c3 |
| docs/experiment-ledger-addendum-c337-preregistration.md | 4ef19a34036a0b28bba0c2f81629da0f4cad32c0 |

No modification to these six files was needed during this review. No accepted C336
or older source, test, contract, log, dispatcher or recovery code is changed. The
pre-activation authoritative handoff is archived by its existing exact blob.

## Checks actually executed after the full reread

Normal own suite: 32/32 PASS, failures/errors/skips 0, 10.165 seconds.
CP932-default-text-open emulation: 32/32 PASS, failures/errors/skips 0, 9.826 seconds.
The emulation supplies CP932 to both builtins.open and io.open only when text
encoding is unspecified; binary and explicitly encoded opens remain unchanged.
All six files decode as UTF-8 without NUL. All three Python files compile/import.
Recursive LOAD_GLOBAL analysis covered 177 function/method/nested code objects;
undefined global bindings: 0. The actual own unittest loader contains 32 methods.
Own ordered test-ID SHA256:
fe8b6d2a2ec5f7a4c80c330bf7e2954fade40ca9735638c5d1773411b7c92c5f.
Manifest self-hash matches:
4233762c9dd30360f0173e22e1db6ec697c1d7cafd479fc3ce6c3bad0ca81d26.

Environment: Linux Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5. The own suite sets
Torch to two threads during its test class. The targeted local tree is NOT a full
repository checkout. It contains the six exact committed child files plus clearly
labelled, local-only verbatim extracts of accepted C336 pure helpers and C267's
canonical dataset writer/constants. These extracts are never committed or used as
replacement historical source in the user's native run. Historical summary checks,
full test inventories, module proofs and OS leases in integration fixtures are
explicit synthetic collaborators. No actual C335 checkpoint/logit evidence, Windows
lock execution, full 6122 historical tests or native PowerShell AST run is claimed.
The real Windows run remains required before a scientific verdict.

Two in-memory negative controls were also run after ordinary tests:
1. Restrict actual predictions to the two supplied values: both test04 and test05
   reject the mutation (two expected errors in total).
2. Mislabel absent catalog values as outside_catalog: test03 and test05 both fail
   their expected-category assertions (two expected assertion failures).
These are deliberate mutant failures, not failures of the reviewed source. All six
source SHA256 values remained unchanged after the controls. No mutant was committed.

## Scientific and parent-writer audit

The accepted C336 R2 logical_groups/classify/aggregate/check_summary and the actual
six-argument semantic_recheck were read. C267's actual dataset writer was also read.
C337's fixture matches the accepted 192 TRAIN / 96 HOLDOUT rows, order, identities
and frozen dataset hash. All twelve distinct ordered value pairs from 0..3 are
covered. The old binary-only assumption is not reintroduced.

The source archive remains fold-c335-evaluations-v1: ten ordered seed/arm records,
native_before evaluation policy, evaluation/replay raw trees and their actual
forward receipts. C336's unchanged semantic reconstruction checks the complete
114-view tree, replay and C335's original negative verdict before the child audit.
C337 then reads only registered normal outputs for its taxonomy. It reconstructs
all 12960 C336 quads and all 720 strata, including row IDs, canonical query/order
orientation, exact predictions, categories and every existing outcome count.
The original 30 HOLDOUT answer/pair/rescue/regression contrasts remain validated
through immediate parent reconstruction; no old verdict or denominator is changed.

Actual prediction remains first-index torch.argmax over all 256 classes. Target and
other supplied identities are used for offline scoring only. Pair margin is target
minus other-supplied logit; support margin is the larger supplied logit minus the
maximum over all 254 other classes. The exclusion occurs in a clone used only for
measurement. Ties use exact zero, with no epsilon, clipping, output repair or
post-hoc threshold. Source and derived nonfinite values are rejected.

Four classes remain correct / wrong_observed / absent_digit / outside_catalog.
Absent_digit means a value from 0..3 absent from this problem, not merely any wrong
answer. Outside_catalog includes ASCII digits 4..9 as well as nondigits; it is not
synonymous with a nondigit or malformed text. A positive pair margin below an
outside winner is NOT a corrected model output or end-to-end accuracy gain.
This diagnostic is not a deployed candidate filter, causal mechanism or Gate F test.

The actual child loader, analysis, writer and semantic reconstruction run against a
complete synthetic ten-state tensor archive and canonical dataset. Test18 exercises
real Torch/JSON reads and four output files and rejects changed saved reconciliation.
All 51840 answers and 720 strata are checked in the full-inventory fixture. Scalar
reference calculations independently verify margins across all twelve value pairs;
256 distinct raw winners and exact tie cases are covered. This is software evidence,
not scientific observations from the user's real saved models.

## Complete protection and execution bridge

Immediate parent identity: C336 execution 274048a72eea1cbb53ece4ec57708e7de2603e6f,
primary31ed3d3e9d45f079bbf4bc200e3a7b5aa82b197cc3f0ded176c01db2b6046b98,
envelope39f2afcdf7107d7e070977e7b4e834694ee77bb68d00cf30a46be15c5c519dcb.
Both parent maps must agree on 877 sources / 4360 inputs. Parent executor and R2
benchmark are byte-pinned before import. Its helper bridge is the actual seven-key
dictionary, not the older C335 tuple. The unchanged parent snapshot reconstructs
inherited inputs; all 461 immediate-parent outputs are added, including 455 module
regression proofs. Six child files yield exactly 883 sources / 4827 inputs.

The finite lock capacity is explicitly max_files=INPUT_COUNT=4827, not the inherited
4096 default and not an unbounded cache. Native R4 leases, independent initial hashes
and all 4827 final uncached rereads are preserved. Test21 uses actual temporary files
for the complete union and rejects altered last-module proof bytes. Test29 requires
the production worker to pass the exact capacity, and exercises worker plus fresh
verifier control flow with explicitly synthetic ancestors/leases/scientific data.

Immediate semantic call is exactly:
C336.semantic_recheck(C336science,C335science,C329data,C335summary,cx,read).
The actual C336 source confirms this six-argument contract; test22 verifies the call
and protected source paths. The original context and canonical prompt validators
run under no_neural. Older semantic bodies are not recursively rerun, but every
inherited file remains protected. The diagnostic makes no new model or optimizer call.

All 6090 original ordered test IDs remain, as confirmed against the published C336
ID digest469a8865f79307ef97c8dba2eac3d87d522f75f80fb7c16e34c64510a9ee5132.
The actual own loader appends 32 tests for 6122 selected / 227 modules, with only the
inherited exact C204 mutable-ACTIVE exclusion. No new omission or cached success.
The production plan validates the entire old ID sequence; author tests exercise this
bridge with explicitly synthetic historical IDs, not the real historical suite.
Accepted R1.2 module execution and evidence checking retain direct/immediate-child
PID relationships, per-test successful IDs and canonical begin/end log markers.
C337 owns its new HEAD/plan/guard and does not invoke the C336-hardcoded module CLI.

Regression failure blocks diagnosis. Four child outputs are hash/size-bound around
saved reconstruction and before writing primary/envelope. A fresh process verifies
complete parent/input/source/output maps, all module proofs, exact manifests and
reconstructed child results. Saved gate false remains valid diagnostic content.

## Launcher and approval boundary

The complete invoke_active_v2 source and both C337 PowerShell files were reread.
Dispatcher resolves the unique Formal-state C337 entry and AST-parses the selected
launcher. The launcher parses itself and the runner before creating scientific logs.
Host, branch, tracked tree, ExpectedHead and ACTIVE checks precede execution/publication.
Runner uses the existing .venv-py31315 interpreter and correct named CLI arguments.
Local output prefix and c337/latest.* publication agree. No environment installation,
new branch, CI, paid service, checkpoint deletion or accepted-model retraining.
No PowerShell executable is present on the author host; native AST success is not
claimed. Mandatory user-side parser checks remain in the standard launch command.

Approval permits one registered C337 run, not a scientific PASS or C338. All 6122
native tests, real saved-artifact checks, child diagnosis, final rereads and independent
verification must still pass. Technical failures stay SAME C337; valid unfavorable
rank distributions are retained. Do not bypass stale/published-command guards.
