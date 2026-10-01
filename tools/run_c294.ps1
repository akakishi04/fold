param(
    [Parameter(Mandatory=$true)][ValidateCount(20,20)][string[]]$Summaries,
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
    Write-Output "=== C294 operational authoring preflight ==="
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c294_saved_support_choice_audit.py") (Join-Path $Root "tests_lm\test_v05_c294_saved_support_choice_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "C294 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c294_saved_support_choice_audit as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 20
b.precheck(paths, Path.cwd())
with b.no_neural():
    p, records, data, metrics = b.load_parent(paths)
    _, summary = b.analyze(records, data, metrics, p["validation_summary"]["final_partitions"])
assert summary["parent_results"] == p["validation_summary"]["seed_results"]
print("real_saved_support_choice_preflight = PASS; no neural execution", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 610; protected_inputs = 1106", flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C294 parent/analysis precheck failed" }
    Write-Output "=== C294 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c294_saved_support_choice_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C294 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c294_saved_support_choice_audit as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C294 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C294 saved support/choice diagnostic ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c294-v5b-support-choice-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c294_saved_support_choice_audit --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C294 diagnostic failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c294_saved_support_choice_audit as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:22]]
head = sys.argv[22]
assert len(sys.argv) == 23 and len(paths) == 20
b.precheck(paths, Path.cwd())
p, report = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("diagnostic_complete =", s["diagnostic_complete"], flush=True)
print("conditional_ranking = ORACLE_SUPPORT_DIAGNOSTIC_ONLY; old gates unchanged", flush=True)
for name in ("partitions", "comparisons"):
    for row in s[name]:
        print("C294", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_support_choice_audit = PASS; model_forward_calls = 0; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C294 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C294 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
