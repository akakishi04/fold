# C215 execution recovery

## Formal disposition

**C215 INVALID EXECUTION / RETRY SAME C215.**
**C216 NOT REGISTERED.**
Gate E remains **PASSED**. Gate F remains **NOT PASSED**.

## Invalid attempt identity

Scientific execution HEAD:
`ea67be1d0916b209038d454cdb607b0479340f6e`

Published log commit:
`6138b515b0862c6cdb93b8622c0e5778cb5161d1`

Log SHA256:
`1f986d85aab2bc87ecf9071b0707b5a98bb9dc9782097b44b8086b4159a4bde2`

## Failure phase

Passed:
- repository preflight;
- Python syntax preflight;
- accepted C214 source/artifact precheck;
-2148 inherited/preceding focused regression tests;
- C215 tests01 through33.

Failed:
- C215 authoring test34 only.

Regression result:

```text
Ran 2149 tests
FAILED (failures=1)
```

The scientific H1/H2 fixture did **not** run.

`run_execution_valid = False`.

## Root cause

`tests_lm.test_v05_c215_h1_h2_chunk_commit.C215Tests.test_34_powershell_guards_and_parent_path`
requires this launcher source contract:

```powershell
$runnerPath = Join-Path $Root "tools\run_c215.ps1"
```

The committed launcher was semantically equivalent but compressed as:

```powershell
$runnerPath=Join-Path $Root "tools\run_c215.ps1"
```

The exact source-level assertion therefore failed.

This is an authoring/launcher formatting mismatch, not scientific evidence about H1/H2 behavior.

## Minimal recovery

Only `tools/invoke_c215.ps1` is changed:

```text
$runnerPath=Join-Path ...
->
$runnerPath = Join-Path ...
```

No changes to:
- C215 manifest;
- scientific question;
- main fixture;
- status sequence;
- H1/H2 counts;
- thresholds;
- parent C214 identity;
- source/protection counts;
- test count;
- regression expected count;
- Gate F interpretation.

Initial recovery patch:
`0b3bed031a71313d9ea2ad670b563394638665d2`

## Recovery review

post_authoring_recovery_review = PASS

review HEAD:
`360b8a448ca94c0bffc33732b059790bfa1de2fd`

Recovery review verified:
- Git compare from published invalid log commit to recovery patch changes only `tools/invoke_c215.ps1`;
- the only launcher change is spacing in the exact `$runnerPath = Join-Path ...` source contract;
- runner,34 tests, H1/H2 source, C215 benchmark and preregistration blobs are unchanged from the invalid execution HEAD;
- the test assertion and launcher now agree on the evaluated PowerShell fragment;
- PowerShell parser preflight remains before execution;
- focused regression count remains2149;
- C215 remains the unique ACTIVE recovery experiment;
- C216 remains unregistered.

Scientific conditions remain frozen.

Retry only after committed remote bytes are re-reviewed.


---

## Second invalid retry attempt

Scientific execution HEAD:
`2204d5dbf56b969daf3aef8d0df68ee9bc7a8eab`

Published log commit:
`31a3852541f554099fb60841d0052cd85f62b448`

Log SHA256:
`1dbd19cfbe5bf75615cbef3f50da33a996183471bad8201392891fae9edaf3f3`

Failure phase:
- repository preflight PASS;
- Python syntax preflight PASS;
- accepted C214 source/artifact precheck PASS;
- C215 tests01-33 PASS;
- C215 test34 ERROR;
- scientific H1/H2 fixture did not run;
- run_execution_valid False.

Regression result:

```text
Ran 2149 tests
FAILED (errors=1)
```

Root cause:
the same source-level guard test also requires the later exact fragment:

```powershell
$failure = $null
```

The retry launcher still used:

```powershell
$failure=$null
```

so the ordering assertion raised `ValueError: substring not found`.

This is again an authoring/launcher formatting mismatch, not scientific evidence.

Second minimal recovery:
only `tools/invoke_c215.ps1` changes:

```text
$failure=$null
->
$failure = $null
```

Patch commit:
`0d60be885b71bfea14d58f066a3ff3922d0fee03`

Git compare from the second published invalid log commit to this patch reports exactly one modified
file, `tools/invoke_c215.ps1`, with one addition and one deletion.

Scientific conditions remain frozen.

## Second recovery review

`post_authoring_recovery_review_2 = PENDING`
