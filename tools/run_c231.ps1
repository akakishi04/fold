param(
    [Parameter(Mandatory=$true)][string]$C230Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c231_byte_eval_contract.py") (Join-Path $Root "tests_lm\test_v05_c231_byte_eval_contract.py")
if ($LASTEXITCODE -ne 0) { throw "C231 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2689 (2690 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; meaningful_language_score = False; training = 0"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c231_byte_eval_contract as b
_, pins, protected = b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS", flush=True)
print("source_pins =", len(pins), "; protected_inputs =", len(protected), flush=True)
'@
& $Python -u -c $Precheck $C230Summary
if ($LASTEXITCODE -ne 0) { throw "C231 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c231_byte_eval_contract as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 116
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2689
r = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c231-v5b-byte-eval-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C231 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c231_byte_eval_contract -v
    if ($LASTEXITCODE -ne 0) { throw "C231 own tests failed; do not run regression or science" }
    Write-Output "authoring_selftest = PASS"
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C231 regression failed; do not run experiment" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.model_c231_byte_eval_contract --c230-summary $C230Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C231 execution failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c231_byte_eval_contract as b
out = Path(sys.argv[1])
b.precheck(Path(sys.argv[2]), Path.cwd())
parent = b.parent_module()
a = parent.context(parent.parent_module()).audit
p = a.read_json(out / "summary.json")
b.validate_result(p)
assert p["commit_sha"] == sys.argv[3]
for name, wanted in p["input_sha256"].items():
    assert a.sha(name) == wanted, name
for item in p["artifacts"]:
    path = a.safe_child(out, item["file"])
    assert a.sha(path) == item["sha256"] and path.stat().st_size == item["serialized_bytes"]
rows = a.read_json(out / "measurements.json")
assert all(b.row_gate(r) for r in rows) == b.gate(p["validation_summary"])
print("=== C231 CONTRACT MEASUREMENTS; UNTRAINED, NOT LANGUAGE ABILITY ===")
print(json.dumps(rows, ensure_ascii=False, indent=2))
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("scientific_status =", p["status"])
s = p["validation_summary"]
for key in ("scored_bytes", "all_contract_checks", "model_forward_calls", "new_training_steps", "meaningful_language_score"):
    print(key, "=", s[key])
print("byte_evaluation_contract_gate =", b.gate(s))
'@
    & $Python -u -c $Postcheck $Out $C230Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C231 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C231 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
