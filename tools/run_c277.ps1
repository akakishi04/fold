param(
    [Parameter(Mandatory=$true)][string]$C276Summary,
    [Parameter(Mandatory=$true)][string]$C275Summary,
    [Parameter(Mandatory=$true)][string]$C274Summary,
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
    Write-Output "=== C277 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"

    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c277_saved_lr_failure_profile_audit.py") (Join-Path $Root "tests_lm\test_v05_c277_saved_lr_failure_profile_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "C277 Python syntax preflight failed" }

    Write-Output "expected_focused_tests = 3813 (3814 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; diagnostic = saved LR failure-profile audit; model_forwards = 0"

    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c277_saved_lr_failure_profile_audit as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path.cwd())
_,metrics=b.load_parent(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
profile,summary=b.audit_metrics(metrics)
assert summary["parent_records"]==10
assert summary["diagnostic_complete"] is True
assert summary["capability_gate_applicable"] is False
print("source_and_artifact_precheck = PASS; source_pins = 508; protected_inputs = 892",flush=True)
print("manifest_sha256 =",b.MANIFEST_SHA,flush=True)
print("saved_lr_audit_preflight = PASS; model_forward_calls = 0; Gate_F = NOT_PASSED",flush=True)
'@
    & $Python -u -c $Precheck $C276Summary $C275Summary $C274Summary
    if ($LASTEXITCODE -ne 0) { throw "C277 parent/task precheck failed" }

    Write-Output "=== C277 own authoring tests: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c277_saved_lr_failure_profile_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C277 own tests failed" }

    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c277_saved_lr_failure_profile_audit as b
modules=b.regression_modules(Path.cwd())
assert len(modules)==len(set(modules))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C277 focused regression preflight ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C277 regression preflight failed" }

    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}

Write-Output "=== C277 saved diagnostic execution ==="
Write-Output "execution_head = $ExpectedHead"
Write-Output "authoring_runtime_preflight = PASS (completed before scientific logging)"
Write-Output "formal_PASS_meaning = saved diagnostic integrity only; no capability winner"
Confirm-Repository

$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c277-v5b-saved-lr-audit-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c277_saved_lr_failure_profile_audit --c276-summary $C276Summary --c275-summary $C275Summary --c274-summary $C274Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C277 saved diagnostic failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c277_saved_lr_failure_profile_audit as b
out,p276,p275,p274,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),sys.argv[5]
b.precheck(p276,p275,p274,Path.cwd())
p,profile=b.verify_artifacts(out,p276,p275,p274,head)
a=b.context()[-1]
print("=== C277 SAVED LR FAILURE-PROFILE AUDIT ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
print("diagnostic_complete =",p["validation_summary"]["diagnostic_complete"])
print("capability_gate_applicable =",p["validation_summary"]["capability_gate_applicable"])
print("parent_seed_pass_counts =",p["validation_summary"]["parent_seed_pass_counts"])
print("parent_two_char_pass_counts =",p["validation_summary"]["parent_two_char_pass_counts"])
print("parent_triple_pass_counts =",p["validation_summary"]["parent_triple_pass_counts"])
print("triple_criterion_delta =",p["validation_summary"]["triple_criterion_delta"])
print("shared_suffix2_holdout_delta =",p["validation_summary"]["shared_suffix2_holdout_delta"])
print("primary =",profile["primary"])
print("persisted_lr_failure_profile = PASS; model_forward_calls = 0")
print("Gate_F = NOT_PASSED; no capability winner is declared")
'@
    & $Python -u -c $Postcheck $Out $C276Summary $C275Summary $C274Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C277 artifact postcheck failed" }

    $Completed = $true
}
finally {
    Write-Output "=== C277 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
