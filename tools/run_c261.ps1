param(
    [Parameter(Mandatory=$true)][string]$C260Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c261_repeated_value_transfer.py") (Join-Path $Root "tests_lm\test_v05_c261_repeated_value_transfer.py")
    if ($LASTEXITCODE -ne 0) { throw "C261 Python syntax preflight failed" }
    Write-Output "python_syntax_preflight = PASS"
    Write-Output "expected_focused_tests = 3429 (3430 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 10; new_training = 0; model_forwards = 540; rows = 95040"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c261_repeated_value_transfer as b
b.precheck(Path(sys.argv[1]),Path.cwd())
b.validate_dataset(b.dataset())
print("source_and_artifact_precheck = PASS; source_pins = 412; protected_inputs = 685",flush=True)
print("repeated_value_dataset_sha256 =",b.DATA_SHA,flush=True)
print("new_assignments = 40; pair_equal_rows = 1296; all_equal_rows = 144",flush=True)
'@
    & $Python -u -c $Precheck $C260Summary
    if ($LASTEXITCODE -ne 0) { throw "C261 parent/task precheck failed" }
    Write-Output "=== C261 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c261_repeated_value_transfer -v
    if ($LASTEXITCODE -ne 0) { throw "C261 own tests failed; do not run regression or evaluation" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c261_repeated_value_transfer as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C261 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C261 regression failed; do not run evaluation" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c261-v5b-repeat-value-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C261 frozen repeated-value evaluation; no training ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c261_repeated_value_transfer --c260-summary $C260Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C261 evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c261_repeated_value_transfer as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,measurements=b.verify_artifacts(out,parent,head)
a=b.context()[-1]
print("=== C261 DECIDING METRICS; FROZEN REPEATED-VALUE TRANSFER ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in measurements:
    print(f'C261 model seed={r["seed"]} arm={r["arm"]} correct={r["correct"]}/{r["rows"]} passed={r["passed"]}')
    for c in r["cells"]:
        print(f'C261 cell seed={r["seed"]} arm={r["arm"]} metrics={c}')
    for c in r["six_order"]:
        print(f'C261 six_order seed={r["seed"]} arm={r["arm"]} metrics={c}')
print("persisted_anchor_new_restoration_replay = PASS; protected_inputs = preserved")
print("C260_valid_negative_unchanged; production_adoption = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C260Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C261 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C261 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
