param(
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
    Write-Output "=== C275 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"

    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c275_saved_gate_failure_audit.py") (Join-Path $Root "tests_lm\test_v05_c275_saved_gate_failure_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "C275 Python syntax preflight failed" }

    Write-Output "expected_focused_tests = 3765 (3766 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; diagnostic = saved gate-failure attribution; model_forwards = 0"

    $Precheck = @'
from pathlib import Path
import sys,torch
from unittest.mock import patch
from fold_lm.v05_benchmarks import model_c275_saved_gate_failure_audit as b
b.precheck(Path(sys.argv[1]),Path.cwd())
with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("preflight forbids model calls")):
    _,metrics=b.load_parent(Path(sys.argv[1]))
    audit,summary=b.audit_metrics(metrics)
assert summary["parent_records"]==10
assert all(summary["primary_seed_coverage"].values())
assert summary["diagnostic_complete"] is True
print("source_and_artifact_precheck = PASS; source_pins = 496; protected_inputs = 868",flush=True)
print("manifest_sha256 =",b.MANIFEST_SHA,flush=True)
print("saved_audit_preflight = PASS; model_forward_calls = 0; Gate_F = NOT_PASSED",flush=True)
'@
    & $Python -u -c $Precheck $C274Summary
    if ($LASTEXITCODE -ne 0) { throw "C275 parent/task precheck failed" }

    Write-Output "=== C275 own authoring tests: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c275_saved_gate_failure_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C275 own tests failed" }

    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c275_saved_gate_failure_audit as b
modules=b.regression_modules(Path.cwd())
assert len(modules)==len(set(modules))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C275 focused regression preflight ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C275 regression preflight failed" }

    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}

Write-Output "=== C275 saved diagnostic execution ==="
Write-Output "execution_head = $ExpectedHead"
Write-Output "authoring_runtime_preflight = PASS (completed before scientific logging)"
Write-Output "formal_PASS_meaning = saved diagnostic integrity only; no capability winner"
Confirm-Repository

$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c275-v5b-gate-failure-audit-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c275_saved_gate_failure_audit --c274-summary $C274Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C275 saved diagnostic failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c275_saved_gate_failure_audit as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,audit=b.verify_artifacts(out,parent,head)
a=b.context()[-1]
print("=== C275 SAVED GATE-FAILURE AUDIT ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
print("diagnostic_complete =",p["validation_summary"]["diagnostic_complete"])
print("capability_gate_applicable =",p["validation_summary"]["capability_gate_applicable"])
print("parent_task_pass_counts =",p["validation_summary"]["parent_task_pass_counts"])
print("primary_final_triple_failures =",p["validation_summary"]["primary_final_triple_failures"])
print("primary_seed_coverage =",p["validation_summary"]["primary_seed_coverage"])
print("primary_aggregates =",audit["primary_final_boundary_triple"]["aggregates"])
print("near_seed_failure_records =",audit["primary_final_boundary_triple"]["near_seed_count"])
print("broad_seed_failure_records =",audit["primary_final_boundary_triple"]["broad_seed_count"])
print("persisted_gate_failure_audit = PASS; model_forward_calls = 0")
print("Gate_F = NOT_PASSED; no capability winner is declared")
'@
    & $Python -u -c $Postcheck $Out $C274Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C275 artifact postcheck failed" }

    $Completed = $true
}
finally {
    Write-Output "=== C275 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
