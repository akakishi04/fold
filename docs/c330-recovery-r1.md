# C330 R1 -- INVALID execution recovery by module-isolated regression

Date: 2026-10-17 Japan time. Same C330 / V5-B-SAVED-GATE-LOCALIZATION.
C330 attempt 1 is INVALID EXECUTION, not a scientific negative or diagnostic PASS.
C329 remains ACCEPTED VALID NEGATIVE. Gate F NOT PASSED. C331 NOT REGISTERED.

## Observed failure and limits of diagnosis

Execution HEAD: 90ba026a0b24beeb448dcb1db354aab3501489bf.
Publication commit: d362e1b654b04fb0a8ee285ddbd9f7ca5f37b6e5.
The publication's sole parent is the execution HEAD. Log publication succeeded.
Publisher metadata: 20290 original Windows bytes; SHA256:
99755b6c4ddfff20f6c144ca63a9b3646e066d1cc034de9b610fcd058e1fa99d.
Log Git blob: 5de6f39cc32721cf92ca249f07c1b90ea364d98d.
Metadata Git blob: 1d115b7f8ec9b1346137a9edf970247cabc4f1b8.
Archive copies: docs/experiment-run-logs/c330/attempt-01/latest.log and latest.json.
The reviewer read exact-ref startup and terminal failure records; no independent
whole-Windows-log rehash, native crash reproduction or memory-dump analysis claimed.

Native read-lock checks, exact C329 parent reconstruction and 838-source/1593-input
registration passed. The 5818-test /219-module full suite was constructed. Its
ordered test-ID SHA256 was:
0e90ec4c1cf292528d7aec95bac8388f12e53fb1ca9dad08ebba58c9174d5183.
The regression process terminated with Windows access violation 0xC0000005
(decimal3221225477), in C311Tests.setUpClass -> model_c311_saved_error_context.py
analyze line139. The Python frame is a list comprehension over saved row data.
This is the observed crash location, NOT proof that C311's Python algorithm, Torch,
CPU, memory hardware, allocator or another specific native library is the cause.

The regression did not return a successful completion receipt. The scientific
worker and controller then returned1 and run_execution_valid=false. Saved C330
localization, child semantic verification and final envelope were not completed.
No C330 diagnostic distribution or capability conclusion may be accepted from this
attempt. The user's PowerShell run_c330.ps1 line19 is error propagation, not the
initial fault. C329's accepted models are not retrained by this repair.

## Bounded operational intervention

Retain the original C330 benchmark, executor, tests, launcher and preregistration
bytes. Change ONLY the Python target in the not-yet-accepted tools/run_c330.ps1
from c330_execution.py to c330_recovery_r1.py. Add the R1 executor,32 recovery tests
and this fixed contract. All C329-and-earlier accepted files are unchanged.
Original C330 diagnostic/source/test artifacts remain available at the failed HEAD.
The original diagnostic-plan.json and its original manifest remain immutable
scientific-definition records; R1 adds a mandatory execution-revision manifest to
both primary result and envelope. Runtime counts/process policy come from R1,
not from the original plan's superseded execution-count fields.

R1 preserves the original 5818 selected test IDs and their ORDER. Their digest must
match the published failed-attempt suite before32 additive tests are appended.
Then partition the full ordered suite by its actual TestCase module, rejecting
missing/duplicate/noncontiguous modules or IDs. Each module runs exactly once in a
new ordinary Python interpreter, sequentially. Preserve all tests and normal
setUpModule/setUpClass/test/tearDownClass/tearDownModule execution within that module.
Do not patch accepted tests, alter assertions, select successful retries, change
Torch optimizer/model behavior, install packages or adjust scientific thresholds.
No new exclusion: the sole inherited exact C204 mutable-ACTIVE test stays excluded.
There is no automatic retry, even when a module exits with an access violation.

This removes cross-module shared-interpreter lifetime/state from the regression.
It is a containment/diagnostic mitigation, not proof that the underlying native
memory fault is fixed. It does NOT claim equivalence to a single-process stress
regression or preservation of cross-module leaked global state. A fresh native
Windows run must establish whether it completes. An isolated crash still INVALIDs
C330 and exposes the exact module, process exit and retained log.

## Full inventory and success evidence

5818 original tests +32 new tests =5850 tests across220 modules.
5851 tests before the unchanged sole inherited C204 exclusion. No test skipping,
cached test successes, parallel module execution or retry-until-PASS loop.

Construct the actual old suite and actual recovery test loader. The original ID
digest and full unique inventory are checked before module execution. A hash-bound
regression-plan-r1.json fixes every module and ordered test ID. Each child verifies
that loading its entire module yields exactly those IDs after the sole exclusion.
The child does not load all other test modules merely to select its own tests.

Track actual startTest and addSuccess IDs. A module succeeds only if the complete
expected ordered sequence both started and passed, with zero failures/errors/skips,
expected failures or unexpected successes. Setup/teardown failures, missing tests,
forged counts and native process exits cannot become aggregate success.

Each new process produces module-NNN.log and module-NNN.json, binding execution HEAD,
plan hash, module index/name, process ID and every actual success ID. The coordinator
requires native exit0 before accepting that receipt. Process IDs are recorded, not
assumed globally unique across OS PID recycling. Receipt/log bytes are hashed into
regression-isolation-r1.json. Only complete5850 success writes regression-result.json.

The scientific worker and fresh final verifier reconstruct the actual suite plan
again (loader construction, not rerunning tests), verify every module receipt/log,
and reconcile the complete5850-success ID sequence and aggregate result. The primary
envelope binds the regression plan/evidence/result hashes. All module evidence is
local-only, not added to model training or committed as scientific data.

## Scientific constants and protection

The existing C330 question, all10 C329 checkpoint records, all5 seeds, both1200/2400
states, six domains, TRAIN/HOLDOUT, profiles, languages and fact orders are unchanged.
4320 local cells,2160 order cells,2160 local transitions,1080 order transitions.
Thresholds .90/.80/.35/.35/.80, parent verdict/count reconstruction and four output
files are unchanged. Diagnostic PASS is integrity, never model capability.
New scientific forwards/gradients/training/optimizer steps/checkpoints remain0.

The unchanged executor blob is1fb5fb47e1e9998cd8ec3a38b25afeb7ec44b31a.
The unchanged benchmark blob is73c30cba137b4d11a9ac39c8f3702bdd0b2e6baf.
Original diagnostic manifest SHA256:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.
R1 operational contract SHA256:
e6bc2750bc4df477e12110ab0c60b2093e5eff985409439ae987d277685448ef.

Immediate accepted parent remains C329 at f8582ca34bd7e10c7403713e935debe94720dfde.
Parent folder: runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/.
Parent science/summary.json SHA256:
89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a.
Parent execution-envelope.json SHA256:
6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.

Full protection:841 sources =832 inherited+6 original C330 own+3 R1 own;
1596 inputs =1577 inherited+10 C329 outputs/summary/envelope+6 C330 own+3 R1 own.
The changed runner is one of the original six own files, never an accepted ancestor.
No reduced source map or hash bypass. Exact C329 semantics are rechecked using the
unchanged parent loader under no_neural. All older protected bytes remain verified;
no recursive older semantic executions or accepted-weight retraining.
Unchanged R4 native read leases remain held through the worker; final uncached
rereads cover all1596 inputs. Scientific outputs are byte-bound before/after saved
reconstruction and again before writing primary/envelope. Fresh verification checks
complete maps, all protected bytes, all module evidence and pure-JSON reconstruction.

Both fold-c330-diagnostic-v1 and fold-c330-execution-envelope-v1 now require
execution_revision='C330-R1', recovery_manifest_sha256 and the exact recovery_manifest
object. The envelope adds regression_isolation, while scientific_work remains the
original zero-neural C330 inventory. A successor must honor both manifests and the
full841/1596 maps; it must not accidentally fall back to original838/1593 counts.

## Authoring and stop boundary

Run the actual32-test loader, compile/import/UTF8/no-NUL/free-global checks and
CP932-default-text-open emulation. Real unittest setup/failure/skip controls, real
subprocess separation and error propagation, and actual worker orchestration are
covered. Large synthetic inventory/parent/lease fixtures must be reported as such.
They are NOT execution of the old5818 tests, native Windows or C311 crash reproduction.
Reread the committed three new files and changed runner, compare Git blobs with
locally tested bytes, rerun tests, and record review before issuing a retry command.
The untouched original C33048 tests are retained for the5850-test native run.

The active dispatcher and invoke_c330 remain unchanged. The user command parses
the dispatcher; dispatcher parses launcher; launcher parses the unchanged-path
run_c330 runner. The runner invokes R1 with the same named CLI parameters and
.venv-py31315 Python. ExpectedHead, branch, unique ACTIVE and tracked-tree guards
remain. Log publication is still C330/latest.*, never a new C number.

Run phases: locked parent -> full module-isolated regression -> unchanged saved
localization -> saved reconstruction ->1596 final rereads -> primary/envelope ->
fresh byte/receipt/JSON verification -> console publication. Scientific progress
has no training step counter. Any module failure stops without retrying or executing
later modules; incomplete envelopes cannot authorize diagnosis/acceptance.
C331 remains NOT REGISTERED. No CI, paid services, package reinstall, model/old-log
mutation or user artifact deletion. Publication-only failure does not rerun diagnosis.
