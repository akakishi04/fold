param(
    [Parameter(Mandatory=$true)][string]$C224Summary,
    [Parameter(Mandatory=$true)][string]$ExpectedHead
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\gate_f_c225_stateful_baseline.py") (Join-Path $Root "tests_lm\test_v05_c225_stateful_baseline.py")
if ($LASTEXITCODE -ne 0) { throw "C225 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2497 (2498 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; measurement_PASS_is_not_superiority = True"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c225_stateful_baseline as b
b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS", flush=True)
'@
& $Python -u -c $Precheck $C224Summary
if ($LASTEXITCODE -ne 0) { throw "C225 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import gate_f_c225_stateful_baseline as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 110
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2497
r = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c225-v5f-stateful-baseline-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C225 own authoring tests first: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c225_stateful_baseline -v
    if ($LASTEXITCODE -ne 0) { throw "C225 own tests failed; do not run regression or science" }
    Write-Output "authoring_selftest = PASS"
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C225 regression failed; do not run comparison" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.gate_f_c225_stateful_baseline --c224-summary $C224Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C225 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c225_stateful_baseline as b
out = Path(sys.argv[1])
b.precheck(Path(sys.argv[2]), Path.cwd())
a = b.parent_module().base_module().audit
p = a.read_json(out / "summary.json")
b.validate_result(p)
assert p["commit_sha"] == sys.argv[3]
for name, wanted in p["input_sha256"].items():
    assert a.sha(name) == wanted, name
for item in p["artifacts"]:
    path = a.safe_child(out, item["file"])
    assert a.sha(path) == item["sha256"] and path.stat().st_size == item["serialized_bytes"]
s = p["validation_summary"]
print("=== C225 MEASUREMENTS ===")
print(b.blob(a.read_json(out / "measurements.json")).decode())
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("scientific_status =", p["status"])
for key in ("history_sizes", "all_quality_parity", "storage_delta_bytes", "storage_smaller_sizes", "query_median_ratio_h1h2_over_symbolic", "raw_query_bytes_candidate", "raw_query_bytes_symbolic"):
    print(key, "=", s[key])
print("stateful_comparison_gate =", b.gate(s))
print("superiority_is_separate = True")
'@
    & $Python -u -c $Postcheck $Out $C224Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C225 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C225 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
