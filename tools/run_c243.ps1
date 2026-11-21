param(
    [Parameter(Mandatory=$true)][string]$C242Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c243_saved_recombination_audit.py") (Join-Path $Root "tests_lm\test_v05_c243_saved_recombination_audit.py")
if ($LASTEXITCODE -ne 0) { throw "C243 Python syntax failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3001 (3002 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; model_forward_calls = 0; new_training_steps = 0"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c243_saved_recombination_audit as b
b.precheck(Path(sys.argv[1]), Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 304; protected_inputs = 466", flush=True)
print("parent_discrete_metric_replay = PASS; nll_recomputed = False", flush=True)
'@
& $Python -u -c $Precheck $C242Summary
if ($LASTEXITCODE -ne 0) { throw "C243 parent/source precheck failed" }
$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c243_saved_recombination_audit as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c243-v5b-saved-recombination-audit-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C243 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c243_saved_recombination_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C243 own tests failed; do not run regression or audit" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C243 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C243 regression failed; do not run audit" }
    Confirm-Repository
    Write-Output "=== C243 saved recombination error audit ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c243_saved_recombination_audit --c242-summary $C242Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C243 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c243_saved_recombination_audit as b
out, parent, head = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
b.precheck(parent, Path.cwd())
p, cells = b.verify_artifacts(out, parent, head)
_, _, a = b.context()
print("=== C243 DECIDING DIAGNOSTICS; SAVED C242 ANSWERS ONLY ===")
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("diagnostic_status =", p["status"])
for key, value in p["validation_summary"].items(): print(key, "=", value)
for c in cells:
    print(f'C243 seed={c["seed"]} family={c["family"]} split={c["split"]} lang={c["language"]} '
          f'rows={c["rows"]} categories={c["categories"]} rule_matches={c["rule_matches"]}')
print("identifiability = TRAIN entity=partner_of_other; HOLDOUT digit categories are exhaustive, not causal evidence")
print("persisted_saved_error_audit_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C242Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C243 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C243 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
