# C330 R1 post-authoring review

Review date: 2026-10-17 Japan time.
post_authoring_review = PASS
Committed recovery source/review target:
64ef391c1869c26d42c90a81f0b757a10097d5ab.
Base invalid-log publication: d362e1b654b04fb0a8ee285ddbd9f7ca5f37b6e5.
This approves the same-C330 recovery implementation for a new native attempt.
It does NOT accept the invalid attempt, claim a scientific result, establish the
native crash's underlying cause or claim that the full5850 tests passed.
Use the subsequent documentation-only final recovery HEAD in the user command.

## Committed-byte reread

The three new protected files and the one-line-modified runner were fetched again
at the exact recovery commit and read completely. Long files were read in consecutive
ranges through EOF. Their returned Git blob IDs match independently computed Git
blob hashes of the local raw files used in the post-reread tests:

| File | Git blob |
|---|---|
| tools/c330_recovery_r1.py | 2c1be72e2d8ff8f9f1e3a51c22a2f99a6402c879 |
| tests_lm/test_v05_c330_recovery_r1.py | 1c35d617598157c5d466ef5a2d1b441ba1340a14 |
| docs/c330-recovery-r1.md | 1d60ffb301ed34e47f0cb177e543e674260aae14 |
| tools/run_c330.ps1 | dc237443640e9ecb886e035628f41d7b6c4da736 |

Remote comparison against the invalid-log publication confirms that the only
existing executable file changed is the not-yet-accepted C330 runner, by one Python
target line. The C330 diagnostic, original executor,48 original tests, original
preregistration and launcher are unchanged. No C329-and-earlier accepted source,
test,log,contract or protected dispatcher is edited. The invalid console/metadata
and pre-recovery handoff are archived as exact Git-blob copies. The prior original
C330 authoring review is retained as history, not silently rewritten.

## Author checks rerun after the full reread

- Normal own suite:32/32 PASS;failures/errors/skips0;3.154seconds.
- CP932-default-text-open emulation:32/32 PASS;failures/errors/skips0;3.246seconds.
  Both builtins.open and io.open supply CP932 only for otherwise unspecified text
  encoding. Binary and explicitly encoded opens are preserved. This is not a native
  Windows/system-locale test.
- All four files are valid UTF-8 without NUL. Both new Python files compile/import.
  Recursive LOAD_GLOBAL checks cover120 code objects,with zero undefined globals.
- The actual new unittest loader contains32 tests. Recovery contract self-hash:
  e6bc2750bc4df477e12110ab0c60b2093e5eff985409439ae987d277685448ef.
- The actual build_plan function was additionally exercised with an explicitly
  synthetic5818-case inherited suite and the real32-test loader. This checks the
  base-helper argument ordering,220-module plan,5850 unique IDs and rejection of a
  changed old-suite digest. The real5850 historical suite was NOT executed here.

Author environment:Linux Python3.13.5. No native Windows crash reproduction,memory
snapshot,full5818/5850 historical regression,actual C329 artifact reconstruction or
C330 scientific diagnostic was performed by these author-side checks. The original
C33048 tests remain unchanged and are retained for the native full run;this review
does not claim to have rerun them locally. No PowerShell executable was available,
so native author-side AST execution is not claimed. User-side AST checks remain.

## Failure diagnosis and scope of mitigation

The exact-ref invalid log records a native access violation0xC0000005 in the long-lived
regression process at C311Tests.setUpClass -> C311.analyze line139. The observed
Python operation is a comprehension over saved row data. It is not evidence that
this Python algorithm itself, a particular library, hardware, optimizer or allocator
is definitively responsible. The error at run_c330.ps1 line19 only propagates the
nonzero child result. No diagnostic result was completed or accepted.

The recovery changes the regression process lifetime:every module receives a fresh
ordinary Python process,once,sequentially. It removes cross-module shared-process
state/lifetime as a condition of the new attempt. It does not claim equivalence to
the old single-process stress test, nor proof that a native fault is cured. A crash
in an isolated module is still INVALID and stops the same C330 with preserved
module-specific evidence. There is no retry-until-PASS loop or omitted C311 test.

## Test inventory and real execution receipts

Before partitioning, build the actual original C330 suite and require the full5818
ordered-ID SHA256 to equal the failed run's published value:
0e90ec4c1cf292528d7aec95bac8388f12e53fb1ca9dad08ebba58c9174d5183.
Append only the actual32 new tests. Group by the real TestCase module,preserving
ordered IDs and rejecting missing/duplicate/noncontiguous modules. Total5850 tests
across220 modules,5851 before the sole inherited exact C204 mutable-ACTIVE exclusion.
No new exclusion,skip,cached success or parallel test-module execution is allowed.

Each child verifies its plan hash and loads its whole module,not a success-selected
subset. Its selected ordered IDs must equal the plan. Real unittest setup/teardown
continues normally within each module. TrackingResult records actual startTest and
addSuccess events. All expected IDs must both start and pass in order,with zero
failures/errors/skips/expected failures/unexpected successes. Setup/teardown errors
and incomplete execution cannot be hidden by aggregate counts or wasSuccessful.

The coordinator observes each child process exit and requires exit0 before checking
its receipt. Each receipt binds HEAD,plan hash,index,module and PID. Exact receipt
and console bytes are hashed into the regression evidence. PID is a recorded process
identity,not a promise that an OS never recycles process numbers. No failure triggers
a second attempt;later modules and diagnosis do not execute after a failed module.
Only complete5850 success writes regression-result.json.

The worker and final verifier independently rebuild the actual full inventory through
loaders without executing tests,and reconcile all recorded started/successful IDs,
per-module counts,process identities,receipt/log hashes and the aggregate digest.
The execution envelope binds the plan,evidence and aggregate receipt hashes.
These receipts establish the module-isolated run,not a monolithic lifetime run.

## Exercised software paths and fixture boundaries

Actual unittest modules created only as explicit test fixtures exercise success,
assertion failure,setUpClass error,skip,expected failure,and ordinary module/class
setup and teardown ordering. They prove that the new accounting does not promote
unrun or failed tests to PASS. Tests reject altered loader IDs,false numeric types,
forged success sequences,wrong process identity and resealed-but-incomplete receipts.

Real subprocesses exercise nonzero exit preservation and the separation of interpreter
globals. They do not reproduce Windows native corruption. Real temporary Git/files
exercise branch/HEAD/dirty-tree guards,UTF8 JSON,exclusive writes,LF/CRLF source hashes
and receipt/log byte tampering. The real module_child dispatch executes one actual
synthetic module and refuses a changed plan before calling test code.

Large220-module/5850-ID collection tests use explicitly synthetic receipts,not a
claim of real historical test execution. The actual scientific_worker control flow
is exercised with explicitly synthetic parent,lease,runtime and diagnostic callbacks.
Its failed-regression variant never invokes diagnosis;the successful variant keeps
diagnostic PASS distinct from the parent's negative capability verdict. The real
controller invokes science then fresh verification only once,retaining failure state.

## Scientific and dependency preservation

All original C330 science remains unchanged:the ten saved C329 states,five seeds,
six domains,both logical splits,all profiles/languages/entity pairs/fact orders,
4320local/2160order cells and2160/1080 transitions. Existing thresholds and complete
parent count/verdict reconstruction remain. New model forwards,gradients,training,
optimizer steps and checkpoint writes remain0. C329 is not rerun or refitted.

The pinned original executor/benchmark are loaded without monkeypatching. Their
actual helpers/snapshot/suite/parent_semantics/bound_semantics interfaces are used.
Helper tuple order is e329,e328,e327,e326,legacy,r4,r6. The R1 full-suite builder calls
the original C330 suite with its existing arguments and extends it additively.
Module children load only their own test module;full-suite construction occurs in
the separate coordinator and receipt-verification paths,not as preloading in every
module child. Accepted test modules may naturally import their declared dependencies.

Protection remains complete:841sources=832 inherited+6 original C330 own+3 R1 own;
1596inputs=1577 inherited+10 immediate C329 files+6 original own+3 R1 own. The revised
runner is one original own path,never an inherited accepted source. Exact parent
summary/envelope and832/1577 maps are validated. The unchanged C329 saved semantic
loader understands its five-trajectories/ten-checkpoints schema. All older protected
bytes are verified without recursively rerunning every older semantic body.

Native unchanged R4 read leases span all worker phases. Every1596 input receives a
final uncached reread. Child output files are hash/size-bound around semantic
reconstruction and before primary/envelope creation. Fresh verification checks the
exact source/input unions,every protected byte,all regression evidence and pure-JSON
diagnostic reconstruction. No input/hash guard is weakened or replaced by a count.

The original scientific manifest and diagnostic-plan.json are retained with original
runtime-count fields as historical scientific-definition records. Both primary and
envelope additionally REQUIRE execution_revision=C330-R1,exact recovery_manifest
and recovery_manifest_sha256. These state the revised5850/220/841/1596 execution
contract;the envelope also requires regression_isolation. A successor must honor
both contracts and the full recovery maps,not revert to original838/1593 protection.

## Retry authorization boundary

This review authorizes the same C330 retry only at the subsequent final reviewed
HEAD. Formal status remains C330 ACTIVE / INVALID ATTEMPT RECOVERY;attempt01 remains
INVALID;C331 remains NOT REGISTERED;Gate F remains NOT PASSED.

The user command parses invoke_active_v2;the unchanged dispatcher parses invoke_c330;
that launcher parses itself and the existing-path run_c330. The runner now points
to c330_recovery_r1.py with unchanged named arguments and .venv-py31315. Branch,
ExpectedHead,unique ACTIVE,tracked-tree and dependency checks remain before logging.
C330 log publication and invalid-attempt archive paths are unchanged.

A native full5850 completion is still required before diagnosis. Isolation may not
resolve the unknown native cause;any further crash remains a same-C330 recovery,
not success or permission to exclude a test. No automatic retry,old-result edits,
C331 registration,CI,paid service,package reinstall or user-artifact deletion.
