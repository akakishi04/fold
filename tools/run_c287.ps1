param(
    [Parameter(Mandatory=$true)][ValidateCount(13,13)][string[]]$Summaries,
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
    Write-Output "=== C287 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c287_saved_fit_partition_audit.py") (Join-Path $Root "tests_lm\test_v05_c287_saved_fit_partition_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "C287 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c287_saved_fit_partition_audit as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 13
b.precheck(paths, Path.cwd())
with b.no_neural():
    _, metrics, fits = b.load_parent(paths)
    _, summary = b.analyze(metrics, fits)
assert summary["parent_results"] == b.expected_results()
assert summary["fixed_records"] == 3240 and len(summary["split_partitions"]) == 60
print("real_partition_schema_dry_run = PASS; no neural execution", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 568; protected_inputs = 1016", flush=True)
print("manifest_sha256 =", b.MANIFEST_SHA, flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C287 parent/schema precheck failed" }
    Write-Output "=== C287 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c287_saved_fit_partition_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C287 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c287_saved_fit_partition_audit as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C287 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C287 saved fit/generalization partition audit ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c287-v5b-fit-partition-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c287_saved_fit_partition_audit --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C287 saved audit failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c287_saved_fit_partition_audit as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:15]]
head = sys.argv[15]
assert len(sys.argv) == 16 and len(paths) == 13
b.precheck(paths, Path.cwd())
p, report = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("diagnostic_complete =", s["diagnostic_complete"], flush=True)
print("capability_gate_applicable = False; model_forward_calls = 0", flush=True)
for name in ("model_partitions", "split_partitions", "loss_bins", "paired_loss_bins"):
    for row in s[name]:
        print("C287", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_fit_partition_audit = PASS; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C287 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C287 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
