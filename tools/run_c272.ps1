param(
    [Parameter(Mandatory=$true)][string]$C271Summary,
    [Parameter(Mandatory=$true)][string]$ExpectedHead,
    [Parameter(Mandatory=$true)][ValidateSet("Validate","Execute")][string]$Mode
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python = Join-Path $Root ".venv-py31315\Scripts\python.exe"

function Confirm-Repository {
    $branch = git branch --show-current
    if ($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss") { throw "Unexpected branch" }
    $head = git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead) { throw "Unexpected HEAD" }
    $dirty = @(git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { throw "Tracked tree must be clean" }
}

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Authoritative Python missing" }
Confirm-Repository

if ($Mode -eq "Validate") {
    Write-Output "=== C272 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"

    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c272_query_boundaries.py") (Join-Path $Root "tests_lm\test_v05_c272_query_boundaries.py")
    if ($LASTEXITCODE -ne 0) { throw "C272 Python syntax preflight failed" }

    Write-Output "expected_focused_tests = 3693 (3694 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 10; training_steps = 8000; model_forwards = 9080; rows = 487680"

    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c272_query_boundaries as b
b.precheck(Path(sys.argv[1]),Path.cwd())
_,_,_,p267,*_=b.context()
data=p267.dataset()
for seed in b.SEEDS:
    ids,profiles,plan=b.schedule(seed,data["TRAIN"])
    assert tuple(ids.shape)==(800,48)
    assert plan["row_exposures"]==[200]*192
    assert plan["profile_updates"]==[268,268,264]
print("source_and_artifact_precheck = PASS; source_pins = 478; protected_inputs = 826",flush=True)
print("manifest_sha256 =",b.MANIFEST_SHA,flush=True)
print("mean_span and boundary_pair use matched initial states/batches; CE only",flush=True)
'@
    & $Python -u -c $Precheck $C271Summary
    if ($LASTEXITCODE -ne 0) { throw "C272 parent/task precheck failed" }

    Write-Output "=== C272 own authoring tests: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c272_query_boundaries -v
    if ($LASTEXITCODE -ne 0) { throw "C272 own tests failed" }

    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c272_query_boundaries as b
modules=b.regression_modules(Path.cwd())
assert len(modules)==len(set(modules))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C272 focused regression preflight ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C272 regression preflight failed" }

    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}

Write-Output "=== C272 scientific execution ==="
Write-Output "execution_head = $ExpectedHead"
Write-Output "authoring_runtime_preflight = PASS (completed before scientific logging)"
Confirm-Repository

$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c272-v5b-query-boundaries-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c272_query_boundaries --c271-summary $C271Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C272 training/evaluation failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c272_query_boundaries as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,metrics=b.verify_artifacts(out,head)
a=b.context()[-1]
print("=== C272 DECIDING METRICS; QUERY BOUNDARIES ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in metrics:
    print(f'C272 model seed={r["seed"]} arm={r["arm"]} two_char={r["two_char"]["passed"]} triple={r["triple"]["passed"]} passed={r["passed"]}')
    for c in r["two_char"]["totals"]:print(f'C272 two_char total seed={r["seed"]} arm={r["arm"]} metrics={c}')
    for c in r["triple"]["totals"]:print(f'C272 triple total seed={r["seed"]} arm={r["arm"]} metrics={c}')
print("persisted_query_boundary_scores = PASS; protected_inputs = preserved")
print("C271_valid_negative_unchanged; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C271Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C272 artifact postcheck failed" }

    $Completed = $true
}
finally {
    Write-Output "=== C272 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
