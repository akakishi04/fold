param(
    [Parameter(Mandatory=$true)][string]$C254Summary,
    [Parameter(Mandatory=$true)][string]$C253Summary,
    [Parameter(Mandatory=$true)][string]$C252Summary,
    [Parameter(Mandatory=$true)][string]$ExpectedHead
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c255_value_residual_swap.py") (Join-Path $Root "tests_lm\test_v05_c255_value_residual_swap.py")
if ($LASTEXITCODE -ne 0) { throw "C255 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3289 (3290 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; training = 0; full_model_forwards = 0; head_forwards = 120; head_rows = 5760"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c255_value_residual_swap as b
parents=[Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])]
b.precheck(*parents,Path.cwd())
b.load_inputs(*parents)
print("source_and_artifact_precheck = PASS; source_pins = 376; protected_inputs = 611",flush=True)
print("C254_archive_replay = PASS; fixed_query_reversed_assignment_donors = PASS",flush=True)
'@
& $Python -u -c $Precheck $C254Summary $C253Summary $C252Summary
if ($LASTEXITCODE -ne 0) { throw "C255 parent/archive precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c255_value_residual_swap as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c255-v5b-value-residual-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C255 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c255_value_residual_swap -v
    if ($LASTEXITCODE -ne 0) { throw "C255 own tests failed; do not run regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C255 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C255 regression failed; do not run diagnostic" }
    Confirm-Repository
    Write-Output "=== C255 frozen fixed-query value-residual diagnostic ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c255_value_residual_swap --c254-summary $C254Summary --c253-summary $C253Summary --c252-summary $C252Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C255 diagnostic failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c255_value_residual_swap as b
out=Path(sys.argv[1])
parents=[Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])]
head=sys.argv[5]
b.precheck(*parents,Path.cwd())
p,diagnostics,contrasts=b.verify_artifacts(out,*parents,head)
_,_,_,_,a=b.context()
print("=== C255 DECIDING DIAGNOSTICS; FIXED QUERY / REVERSED VALUES ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("diagnostic_status =",p["status"])
for k,v in p["validation_summary"].items(): print(k,"=",v)
for c in contrasts: print("C255 contrast =",c)
print("coherent_swap = donor_logit_replay_control_only; not_recipient_accuracy")
print("persisted_value_swap_and_coherent_donor_replay = PASS; protected_inputs = preserved")
print("C252_C253_C254_verdicts_unchanged; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C254Summary $C253Summary $C252Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C255 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C255 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
