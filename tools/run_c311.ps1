param(
    [Parameter(Mandatory=$true)][ValidateCount(37,37)][string[]]$Summaries,
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
    Write-Output "=== C311 authoring preflight ==="
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c311_saved_error_context.py") (Join-Path $Root "tests_lm\test_v05_c311_saved_error_context.py")
    if ($LASTEXITCODE -ne 0) { throw "C311 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c311_saved_error_context as b
paths = [Path(p) for p in sys.argv[1:]]
assert len(paths) == 37
b.runtime_preflight(paths, Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 712; protected_inputs = 1333", flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C311 parent/value-alignment precheck failed" }
    Write-Output "=== C311 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c311_saved_error_context -v
    if ($LASTEXITCODE -ne 0) { throw "C311 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c311_saved_error_context as b
assert len(b.regression_modules(Path.cwd())) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C311 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C311 saved error-context diagnostic ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c311-v5b-error-context-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c311_saved_error_context --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C311 diagnostic execution failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c311_saved_error_context as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:39]]
head = sys.argv[39]
assert len(sys.argv) == 40 and len(paths) == 37
b.precheck(paths, Path.cwd())
p, report = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[-1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("diagnostic_complete =", s["diagnostic_complete"], flush=True)
print("observations =", s["observations"], flush=True)
print("pair_groups =", s["pair_groups"], "signature_groups =", s["signature_groups"], flush=True)
for row in report["pairs"]:
    if row["seed"] == 309002 and row["identifier_length"] == 5 and row["split"] == "HOLDOUT":
        print("C311 focus_heldout_pair", json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
for row in report["length_signatures"]:
    if row["seed"] == 309002 and row["split"] == "HOLDOUT":
        print("C311 focus_length_signature", json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_error_context = PASS; model_forward_calls = 0; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C311 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C311 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
