param(
    [Parameter(Mandatory=$true)][ValidateCount(39,39)][string[]]$Summaries,
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
    Write-Output "=== C313 authoring preflight ==="
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c313_frozen_six_transfer.py") (Join-Path $Root "tests_lm\test_v05_c313_frozen_six_transfer.py")
    if ($LASTEXITCODE -ne 0) { throw "C313 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c313_frozen_six_transfer as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 39
b.runtime_preflight(paths, Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 724; protected_inputs = 1357", flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C313 parent/six-frame precheck failed" }
    Write-Output "=== C313 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c313_frozen_six_transfer -v
    if ($LASTEXITCODE -ne 0) { throw "C313 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c313_frozen_six_transfer as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C313 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C313 frozen six-character transfer ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c313-v5b-frozen-six-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c313_frozen_six_transfer --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C313 scientific execution failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c313_frozen_six_transfer as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:41]]
head = sys.argv[41]
assert len(sys.argv) == 42 and len(paths) == 39
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[-1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("primary_arm =", s["primary_arm"], flush=True)
print("primary_gate =", s["primary_gate"], flush=True)
print("six_pass_counts =", json.dumps(s["six_pass_counts"], sort_keys=True), flush=True)
for name in ("seed_results", "final_partitions", "five_to_six", "reproductions"):
    for row in s[name]:
        print("C313", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("all_replays =", s["all_replays"], flush=True)
print("persisted_frozen_six = PASS; train_steps = 0; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C313 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C313 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
