param(
    [Parameter(Mandatory=$true)][ValidateCount(35,35)][string[]]$Summaries,
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
    Write-Output "=== C309 authoring preflight ==="
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c309_core_lr_replication.py") (Join-Path $Root "tests_lm\test_v05_c309_core_lr_replication.py")
    if ($LASTEXITCODE -ne 0) { throw "C309 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c309_core_lr_replication as b
paths = [Path(p) for p in sys.argv[1:]]
assert len(paths) == 35
b.runtime_preflight(paths, Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 700; protected_inputs = 1309", flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C309 parent/policy/optimizer precheck failed" }
    Write-Output "=== C309 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c309_core_lr_replication -v
    if ($LASTEXITCODE -ne 0) { throw "C309 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c309_core_lr_replication as b
assert len(b.regression_modules(Path.cwd())) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C309 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C309 unchanged core-LR fresh-seed replication ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c309-v5b-core-lr-replication-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c309_core_lr_replication --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C309 scientific execution failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c309_core_lr_replication as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:37]]
head = sys.argv[37]
assert len(sys.argv) == 38 and len(paths) == 35
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[-1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("candidate_gate =", s["candidate_gate"], flush=True)
print("length_pass_counts =", json.dumps(s["length_pass_counts"], sort_keys=True), flush=True)
print("paired_five =", json.dumps(s["paired_five"], sort_keys=True), flush=True)
for name in ("seed_results", "final_partitions", "contrasts", "gradient_receivers"):
    for row in s[name]:
        print("C309", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("all_groups_matched =", s["all_groups_matched"], flush=True)
print("persisted_core_lr_replication = PASS; primary = new-cohort-unseen-five; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C309 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C309 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
