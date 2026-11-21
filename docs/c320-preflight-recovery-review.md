# C320 preflight recovery 1 — diagnostic observability, not an established root-cause fix

post_authoring_review = PASS (operational delta only)
Original active HEAD:ead33368286ae4539fabf0e264651e98858a136c.
Recovery authoring/review target:e5e0a07e5ebfd0816f0f26c0cc757ed2f31b1f52.
C320 has no scientific result. C319 remains ACCEPTED VALID NEGATIVE;C321 NOT REGISTERED.

## Evidence actually available

User-reported C320 preflight ends after C173 test36 with all shown C172/C173 tests marked ok.
It reports AUTHORING_RUNTIME_PREFLIGHT_FAILED / C320 focused regression failed,
experiment_executed=False and execution_log_publish_attempted=False. No terminal unittest
summary or traceback was present in the supplied tail. The original Python exit code is unknown.
This is one supplied failed attempt;re-reading its tail is not evidence of repeated executions.
Do not identify C173 or C174 as the failed test solely from the final printed successful test.

The user then ran ONLY tests_lm.test_v05_c174_learned_necessity.C174Tests.test_01_exact_dependency_copy
in a new authoritative Python process with -X faulthandler. Report:Ran1test in3.525s,OK,
exit_code_decimal=0,exit_code_hex=0x00000000.
Probe log reported at runs/c320-c174-probe-e44a2b5fc4fb45ec88526968521ef5af.log.
This proves that this isolated setup+first-test invocation completed. It does not prove the
entire C174 module or original 5221-test process completed. Order-dependent state,resource
conditions or an external/native interruption remain possibilities,not diagnosed causes.
The local failed preflight/probe files have not been fetched by the assistant and were not
published as scientific logs. Do not fabricate an INVALID science summary or a capability FAIL.

## Minimal operational delta

Only tools/run_c320.ps1 and tools/invoke_c320.ps1 change at the review target.
The scientific Python source,24 own tests,preregistration,design,manifest,data,models,scoring,
full205-module/5222-loaded/5221-focused suite and exact inherited C204 exclusion are unchanged.
The scientific Execute/postcheck portion of run_c320.ps1 is byte-identical. All46 ancestor
paths and CLI postcheck indices [2:48]/head48/argc49 are unchanged. No environment reinstall,
thread-setting change,per-module subprocess splitting,test retry loop or test filtering.

The regression child still builds the actual C320 regression_suite and executes it once in
one process. It checks the same ordered test IDs before wrapping the flat suite. ObservedSuite
only brackets the inherited unittest module/class setup/teardown methods with flushed markers;
the superclass still performs the original fixtures/cleanup. The original wasSuccessful result
still determines normal success/failure. Exceptions propagate and are printed,not suppressed.
These observer markers add I/O/timing overhead;they cannot rule out timing-sensitive failures.

A unique runs/c320-regression-<guid>.log is opened exclusively in UTF-8 before suite import.
Unittest output and fixture markers are written directly there and also to the console.
faulthandler targets that open descriptor during regression;the handler returns to stderr before
the descriptor closes. This improves evidence for supported fatal errors but cannot guarantee
traceback capture for every OS kill,power loss or arbitrary native termination.
PowerShell captures LASTEXITCODE immediately after the regression child and writes decimal,
unsigned32-bit hexadecimal and the direct-log path before any subsequent git command. Nonzero
exit prints the last35 direct-log lines and throws with the exact code/path. The existing
Validate failure path still skips scientific Execute/publication. The launcher copies the old
c320-preflight-last.log to a unique previous log BEFORE Tee-Object starts the next preflight.

## Post-commit byte review and tests actually executed

Both complete changed files were fetched from the immutable review target after commit.
Returned Git blob IDs matched independently hashed local tested bytes:
- tools/run_c320.ps1:006154cb0cbeada61132f2c8d5d68395503587d3;9221bytes.
- tools/invoke_c320.ps1:e5c7cfefb4fbc08ac050141cb96f51614b1196c5;8397bytes.
Remote comparison/commit diff contains only these2 script changes. Unchanged OWN4 and all
accepted ancestors therefore retain their original reviewed byte identities.

After refetch,7 local operational regression-observer test methods ran:7/7 PASS in17.842s,
zero failures/errors,process exit0. Linux/Python3.13.5. These are NOT the registered C320 own24
or the actual inherited5221 tests. No claim those real tests passed in this recovery review.

The controls compared standard unittest and the observed runner on identical controlled
fixtures under normal and CP932-default emulation. Success,assertion failure,skip,subtest
failure,class-setup failure and teardown failure preserve exact event order and exit outcome.
Additional subprocess controls verify duplicate-ID rejection before tests,SystemExit23
propagation,os._exit37 leaving the flushed last setup boundary,and a controlled Linux native
abort leaving faulthandler's stack in the direct log. These artificial failures are tests of
logging,not a reproduction of the user's unknown failure. Existing log overwrite is rejected.

All3 embedded Python blocks compile;unchanged precheck/postcheck blocks and the complete
scientific Execute tail are checked for byte equality. The standalone local test harness uses
synthetic modules,not the FOLD repository/checkpoints,and is not part of the scientific suite.
No native PowerShell executable is available here:PowerShell ParseFile,the user's actual
runtime,46parent archives,own24/full5221 and scientific evaluation remain user-side gates.
The existing dispatcher->launcher->runner ParseFile chain remains mandatory and unchanged.

## Scope and retry

This review authorizes the standard guarded SAME-C320 retry,not a claim that the original
failure's root cause is repaired. ExpectedHead must be the later documentation/recovery HEAD.
No C321 registration. If full Validate passes,the unchanged C320 evaluation may proceed and
publish normally. If it stops again,use the new exact native code,fixture boundary and direct
log;do not skip a test or keep retrying without inspecting the evidence.
Science remains frozen10models,3420forwards,328320rows,13680core calls,training0;source766/input1443.
Both original layouts,mean_last primary,all5 requirement,local/masked gates and Gate F unchanged.
