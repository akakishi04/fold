# C330 R1.2 -- bind launcher and runtime identities without assuming equal PIDs

Date:2026-10-18 Japan time. SAME C330 / V5-B-SAVED-GATE-LOCALIZATION.
C330 remains ACTIVE / INVALID ATTEMPT RECOVERY. C329 ACCEPTED VALID NEGATIVE.
Gate F NOT PASSED. C331 NOT REGISTERED. No C330 scientific verdict exists.
This supersedes unaccepted R1.1 execution mechanics only. Its contract and handoff
are archived as docs/handoff-history/c330-r1.1-contract.md and c330-r1.1-prepatch.md.
Earlier attempts and reviews remain in history, not retroactively accepted evidence.

## Attempt03 and the duplicate-invocation message

Failed execution:848117fe8326ff146c350343b69d00858a6b0743.
Log publication:63195b8948375de6917e55e692c7bc7b8f01d4ce;sole parent equals execution.
Publisher metadata:7472 original Windows bytes;SHA256
6da276291662559fdcc268933f6466c1a13904d11a77a9ffdc705cb830739928.
Log blob:bf236eaedd498b93c504ba86dedef267044f6b20.
Metadata blob:8a0786ea37e18b94bda06a7900d34b936f0fbd75.
Exact copies:docs/experiment-run-logs/c330/attempt-03/latest.log and latest.json.
Local folder:runs/c330-localization-fd85cb97845948b788d5cb35b8c4b374/.

Native locks, accepted C329 semantic verification and841source/1596input registration
passed. The full5850-ID plan was built with digest
f7c7f355197393a53f0d9d8f3f4c8a044e4b365719a4894090017e206e709dc6.
The first module tests_lm.test_v05_controller ran10tests in0.009s,all successful.
Its runtime printed PID1304. The Popen launch process returned PID45276 and exit0.
collect_regression required those PIDs to be equal and raised
ValueError:module process identity. No module1 or diagnostic was reached; no full
regression receipt exists. Regression/science exit1;run_execution_valid=false.
This attempt does not reproduce the earlier C311 access violation.

The later RESULT_ALREADY_PUBLISHED invocation is an operational guard:it starts no
experiment and publishes nothing. It is neither a new invalid attempt nor a PASS.
Do not substitute the publication HEAD into an old command to bypass that guard.

## Root cause and evidence boundary

The confirmed software error is the equality assumption between subprocess.Popen.pid
and the interpreter's os.getpid(). CPython's Windows venv launcher locates the base
Python, calls CreateProcessW, waits for that process, and returns its exit code.
Its launch process and runtime therefore need not have the same PID.
Primary reference:CPython3.13 PC/venvlauncher.c,launch(),especially CreateProcessW,
WaitForSingleObjectEx and GetExitCodeProcess:
`https://raw.githubusercontent.com/python/cpython/3.13/PC/venvlauncher.c`
Documentation:`https://docs.python.org/3.13/library/venv.html`.

Attempt03 did not record the runtime's parent PID. Thus the mismatch is observed,
while attributing those two particular processes to the documented redirector is
source-supported interpretation,not a recovered OS process-tree measurement.
R1.2 captures parent PID explicitly. It does not diagnose CPU/RAM failure or prove
the initial C311 native exception fixed. This is an authoring error in the harness.

## Minimal repair and bounded process topology

Only the unaccepted recovery executor,test module and this execution contract change.
Keep their paths:tools/c330_recovery_r1.py,tests_lm/test_v05_c330_recovery_r1.py,
docs/c330-recovery-r1.md. No runner/launcher/dispatcher/accepted scientific file edits.

Capture os.getpid() and os.getppid() before a test module runs. Require both remain
unchanged after tests. The collector separately retains the Popen launch PID and
accepts exactly one of these relationships:
- direct:launcher_pid==worker_pid;
- redirected-child:launcher_pid==worker_parent_pid and launcher_pid!=worker_pid.
All IDs must be positive integers,not bools;worker_pid!=worker_parent_pid.
Unrelated processes and deeper undocumented launcher chains fail closed with all
three IDs in the error message. No wildcard PID acceptance or silent retry.

Module begin and complete records include the same worker/parent IDs. The collector
and fresh verifier use one validator to require the exact module schema,HEAD,plan
hash,index,module name,all started/successful test IDs and both canonical log markers.
Missing/duplicate markers,log/receipt disagreement,unknown fields,incomplete success,
nonzero exit or invalid PID topology abort. Resealing a changed log hash does not
bypass semantic marker validation. Aggregate evidence separately stores launcher_pid,
pid(worker),parent_pid,relation and exit_code,plus receipt/log hashes. Fresh verification
revalidates the same topology and exact receipt identities. This is cooperative
process evidence,not cryptographically signed OS ancestry or protection from arbitrary
malicious local code. A different PID alone is neither success nor failure.

Module receipt schema becomes fold-c330-r1-module-v2;aggregate isolation schema
fold-c330-r1-regression-v2. The plan schema remains fold-c330-r1-regression-plan-v1.
Filenames retain r1 for the existing route. Primary/envelope must both require
execution_revision=C330-R1.2,exact recovery_manifest and SHA256:
cb09791f16e446ad2e1116981700c5be26997865d2da2eef89e76acdad1df8b9.
Old module-v1 evidence cannot satisfy this revision. No accepted R1 result is lost;
all previous R1 attempts were invalid.

## Unchanged regression and scientific contracts

Original5818 ordered-ID SHA remains
0e90ec4c1cf292528d7aec95bac8388f12e53fb1ca9dad08ebba58c9174d5183.
The same32 recovery test method IDs remain; strengthen their cases without removing
existing failure/skip/namespace/count/fixture checks. Full5850tests/220modules remain
required,5851 before the sole inherited exact C204 mutable-ACTIVE exclusion.
Keep the three exact tests_tools modules and their registry check;no new exclusion.
One fresh ordinary interpreter per module,sequentially,once only. Every planned ID
must actually start and succeed. No cached success or cross-module shared-process
stress-equivalence claim. All5850must pass before C330 diagnosis.

C330 scientific manifest unchanged:
f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7.
Benchmark73c30cba137b4d11a9ac39c8f3702bdd0b2e6baf;
base executor1fb5fb47e1e9998cd8ec3a38b25afeb7ec44b31a.
All10C329 checkpoints,5seeds,1200/2400steps,sixdomains,TRAIN/HOLDOUT,allprofiles,
languages,entity sets,orders and thresholds.90/.80/.35/.35/.80 remain fixed.
4320local/2160order cells and2160local/1080order transitions. New scientific fitting,
model forwards,gradients,optimizer steps and checkpoints remain0. No C329 retraining.
Diagnostic PASS concerns integrity only;C329 remains VALID NEGATIVE and Gate F fails.

## Parent, protection and author validation

C329 execution:f8582ca34bd7e10c7403713e935debe94720dfde.
Folder:runs/c329-budget-66a7cc83726341aaa59542f02bc7a7e5/.
PrimarySHA89341eade41d5c35c2e7b9a7a84238b272adcd21c28d143da68fbc0aaf8fdf1a.
EnvelopeSHA6939cb8c53a44ffefd86342721d48d168e7c938f37432948ea3488fe1453b473.
Use its unchanged five-trajectory/ten-state semantic loader under no_neural.
No older semantic recursion;all inherited bytes still protected.
841sources=832parent+6C330own+3recovery;
1596inputs=1577parent+10immediate-parent files+6C330own+3recovery.
Native R4 read leases,initial independent hashes,all1596final uncached rereads,
four hash-bound diagnostic outputs and fresh byte/receipt/JSON verification remain.

Author tests must exercise real OS processes through the production module CLI,
collector and fresh verifier,not only PID mocks. Test direct and deliberate one-hop
proxy launches,plus a failing proxy child whose exit must propagate and stop at the
first module. For stdlib-only fixtures,sys._base_executable avoids an extra implicit
venv shim around the deliberately added proxy;the scientific runner is unchanged.
Large inventory/other module receipts remain explicitly synthetic. These fixtures
are not a native Windows venv run,actual C329 diagnosis or full5850regression.
Retain source/UTF8/NUL/compile/import/free-global audits and CP932-default-open testing.
Reread all3 committed changed files and compare their Git blobs to tested local bytes,
then rerun tests before post-authoring review PASS and a user retry command.

## Invocation and stops

Existing active_v2 ->invoke_c330 ->run_c330 ->c330_recovery_r1.py route is unchanged.
Role:C330-R1.2-MODULE-ISOLATED-RECOVERY. Parent checks ->5850module-isolated tests
->unchanged diagnosis ->1596final rereads ->fresh verifier ->console publication.
New regression_process_identity reports launch/runtime/parent IDs and their relation.
Do not interpret per-module OK or log publication as complete PASS.
Any PID/namespace/test/native/source/input/receipt/schema/semantic mismatch stops
SAME C330,no automatic retry or C331. Keep all attempt archives. Publication-only
failure repairs publication alone. No reinstall,paidservice,CI,artifact deletion,
accepted-source change,model selection or weakened scientific gate.
