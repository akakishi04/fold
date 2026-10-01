param(
    [Parameter(Mandatory=$true)][ValidateCount(18,18)][string[]]$Summaries,
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
    Write-Output "=== C292 operational authoring preflight ==="
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c292_saved_answer_roles.py") (Join-Path $Root "tests_lm\test_v05_c292_saved_answer_roles.py")
    if ($LASTEXITCODE -ne 0) { throw "C292 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c292_saved_answer_roles as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 18
b.precheck(paths, Path.cwd())
with b.no_neural():
    parent, records, data, metrics = b.load_parent(paths)
    _, summary = b.analyze(records, data, metrics)
assert summary["parent_results"] == parent["validation_summary"]["seed_results"]
print("real_saved_role_audit_preflight = PASS; no neural execution", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 598; protected_inputs = 1081", flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C292 parent/role precheck failed" }
    Write-Output "=== C292 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c292_saved_answer_roles -v
    if ($LASTEXITCODE -ne 0) { throw "C292 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c292_saved_answer_roles as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C292 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C292 saved answer-role audit ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c292-v5b-answer-roles-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c292_saved_answer_roles --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C292 diagnostic failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c292_saved_answer_roles as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:20]]
head = sys.argv[20]
assert len(sys.argv) == 21 and len(paths) == 18
b.precheck(paths, Path.cwd())
p, report = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("diagnostic_complete =", s["diagnostic_complete"], flush=True)
for name in ("partitions", "value_pairs", "comparisons"):
    for row in s[name]:
        print("C292", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_answer_role_audit = PASS; model_forward_calls = 0; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C292 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C292 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
