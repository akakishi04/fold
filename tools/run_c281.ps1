param(
    [Parameter(Mandatory=$true)][ValidateCount(7,7)][string[]]$Summaries,
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
    Write-Output "=== C281 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c281_saved_support_transition_audit.py") (Join-Path $Root "tests_lm\test_v05_c281_saved_support_transition_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "C281 Python syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c281_saved_support_transition_audit as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 7
b.precheck(paths, Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 532; protected_inputs = 940", flush=True)
print("manifest_sha256 =", b.MANIFEST_SHA, flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C281 parent precheck failed" }
    Write-Output "=== C281 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c281_saved_support_transition_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C281 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c281_saved_support_transition_audit as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C281 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C281 saved diagnostic execution ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c281-v5b-saved-support-audit-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c281_saved_support_transition_audit --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C281 saved audit failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c281_saved_support_transition_audit as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:9]]
head = sys.argv[9]
assert len(sys.argv) == 10 and len(paths) == 7
b.precheck(paths, Path.cwd())
p, report = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[-1].sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
print("diagnostic_complete =", p["validation_summary"]["diagnostic_complete"], flush=True)
print("capability_gate_applicable = False; model_forward_calls = 0", flush=True)
for name, data in report["primary"].items():
    print("C281 primary", name, json.dumps(data, sort_keys=True, separators=(",", ":")), flush=True)
for seed, data in report["per_seed_triple"].items():
    print("C281 seed", seed, json.dumps(data, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_support_transition_audit = PASS; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C281 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C281 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
