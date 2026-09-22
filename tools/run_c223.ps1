param(
    [Parameter(Mandatory=$true)][string]$C222Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05\memory_request_lease.py") (Join-Path $Root "fold_lm\v05_benchmarks\gate_f_c223_request_freshness.py") (Join-Path $Root "tests_lm\test_v05_c223_request_freshness.py")
if ($LASTEXITCODE -ne 0) { throw "C223 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2435 (2436 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; no_training = True"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c223_request_freshness as b
b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS", flush=True)
'@
& $Python -u -c $Precheck $C222Summary
if ($LASTEXITCODE -ne 0) { throw "C223 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import gate_f_c223_request_freshness as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 108
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2435
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c223-v5f-request-freshness-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C223 own authoring tests first: 34 ==="
    & $Python -u -m unittest tests_lm.test_v05_c223_request_freshness -v
    if ($LASTEXITCODE -ne 0) { throw "C223 own tests failed; do not run historical regression or science" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C223 regression failed; do not run request freshness" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.gate_f_c223_request_freshness --c222-summary $C222Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C223 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c223_request_freshness as b
out = Path(sys.argv[1])
b.precheck(Path(sys.argv[2]), Path.cwd())
a = b.parent_module().parent_module().parent_module().audit
p = a.read_json(out / "summary.json")
b.validate_result(p)
assert p["commit_sha"] == sys.argv[3]
for name, wanted in p["input_sha256"].items():
    assert a.sha(name) == wanted, name
for artifact in p["artifacts"]:
    path = a.safe_child(out, artifact["file"])
    assert a.sha(path) == artifact["sha256"] and path.stat().st_size == artifact["serialized_bytes"]
s = p["validation_summary"]
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("scientific_status =", p["status"])
for key in ("fresh_success", "parent_parity", "stale_success", "stale_result_exposures", "repeat_success", "replay_success", "stale_calls"):
    print(key, "=", s[key])
print("freshness_gate =", b.gate(s))
'@
    & $Python -u -c $Postcheck $Out $C222Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C223 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C223 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
