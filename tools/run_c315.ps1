param(
    [Parameter(Mandatory=$true)][ValidateCount(41,41)][string[]]$Summaries,
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
    Write-Output "=== C315 authoring preflight ==="
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c315_single_character_mix.py") (Join-Path $Root "tests_lm\test_v05_c315_single_character_mix.py")
    if ($LASTEXITCODE -ne 0) { throw "C315 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c315_single_character_mix as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 41
b.runtime_preflight(paths, Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 736; protected_inputs = 1379", flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C315 parent/single-character precheck failed" }
    & $Python -u -m unittest tests_lm.test_v05_c315_single_character_mix -v
    if ($LASTEXITCODE -ne 0) { throw "C315 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c315_single_character_mix as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C315 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C315 single-character training mix ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c315-v5b-single-mix-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c315_single_character_mix --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C315 scientific execution failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c315_single_character_mix as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:43]]
head = sys.argv[43]
assert len(sys.argv) == 44 and len(paths) == 41
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[-1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
print("candidate_gate =", s["candidate_gate"], flush=True)
print("length_pass_counts =", json.dumps(s["length_pass_counts"], sort_keys=True), flush=True)
print("paired_six =", json.dumps(s["paired_six"], sort_keys=True), flush=True)
for name in ("seed_results", "final_partitions", "single_character_diagnostics"):
    for row in s[name]:
        print("C315", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("all_pairs_matched =", s["all_pairs_matched"], flush=True)
print("persisted_single_mix = PASS; primary = unseen-six; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C315 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C315 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
