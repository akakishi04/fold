param(
    [Parameter(Mandatory=$true)][string]$C257Summary,
    [Parameter(Mandatory=$true)][string]$C256Summary,
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
$Completed = $false
try {
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c258_saved_middle_slot_audit.py") (Join-Path $Root "tests_lm\test_v05_c258_saved_middle_slot_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "C258 Python syntax preflight failed" }
    Write-Output "python_syntax_preflight = PASS"
    Write-Output "expected_focused_tests = 3357 (3358 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; new_training = 0; model_forwards = 0; attributed_rows = 8640"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c258_saved_middle_slot_audit as b
b.precheck(Path(sys.argv[1]),Path.cwd())
with b.no_model_calls():
    b.context()[0].load_inputs(Path(sys.argv[2]))
print("source_and_artifact_precheck = PASS; source_pins = 394; protected_inputs = 647",flush=True)
print("C257 accepted valid negative; no new capability gate",flush=True)
'@
    & $Python -u -c $Precheck $C257Summary $C256Summary
    if ($LASTEXITCODE -ne 0) { throw "C258 parent precheck failed" }
    Write-Output "=== C258 own authoring tests first: 20 ==="
    & $Python -u -m unittest tests_lm.test_v05_c258_saved_middle_slot_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C258 own tests failed; do not run regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c258_saved_middle_slot_audit as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C258 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C258 regression failed; do not run diagnostic" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c258-v5b-middle-slot-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C258 saved-output audit; no new model inference ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c258_saved_middle_slot_audit --c257-summary $C257Summary --c256-summary $C256Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C258 diagnostic failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c258_saved_middle_slot_audit as b
out,p257,p256,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
b.precheck(p257,Path.cwd())
p,signatures=b.verify_artifacts(out,p257,p256,head)
a=b.context()[3]
print("=== C258 DECIDING METRICS; EXPLORATORY SAVED-ANSWER ATTRIBUTION ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"],"; diagnostic integrity only")
for k,v in p["validation_summary"].items():print(k,"=",v)
for row in signatures:print("C258 signature =",row)
print("persisted_row_and_signature_recomputation = PASS; protected_inputs = preserved")
print("C257_valid_negative_unchanged; capability_pass_claim = False; causal_mechanism_claim = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C257Summary $C256Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C258 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C258 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
