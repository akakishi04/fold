param(
    [Parameter(Mandatory=$true)][string]$C263Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c264_two_fact_deletion.py") (Join-Path $Root "tests_lm\test_v05_c264_two_fact_deletion.py")
    if ($LASTEXITCODE -ne 0) { throw "C264 Python syntax preflight failed" }
    Write-Output "python_syntax_preflight = PASS"
    Write-Output "expected_focused_tests = 3501 (3502 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 20; new_training = 0; model_forwards = 600; rows = 120960"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c264_two_fact_deletion as b
b.precheck(Path(sys.argv[1]),Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 430; protected_inputs = 723",flush=True)
print("two_fact_dataset_sha256 =",b.DATA_SHA,flush=True)
print("unique_new_rows = 288; provenance_edges = 1728; new_training = 0",flush=True)
'@
    & $Python -u -c $Precheck $C263Summary
    if ($LASTEXITCODE -ne 0) { throw "C264 parent/task precheck failed" }
    Write-Output "=== C264 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c264_two_fact_deletion -v
    if ($LASTEXITCODE -ne 0) { throw "C264 own tests failed; do not run regression or evaluation" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c264_two_fact_deletion as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C264 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C264 regression failed; do not run evaluation" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c264-v5b-two-fact-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C264 frozen two-fact evaluation; no training ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c264_two_fact_deletion --c263-summary $C263Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C264 evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c264_two_fact_deletion as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,measurements=b.verify_artifacts(out,parent,head)
a=b.context()[-1]
print("=== C264 DECIDING METRICS; FROZEN TWO-FACT DELETION ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in measurements:
    print(f'C264 model seed={r["seed"]} arm={r["arm"]} correct={r["correct"]}/{r["rows"]} passed={r["passed"]}')
    for c in r["cells"]:print(f'C264 cell seed={r["seed"]} arm={r["arm"]} metrics={c}')
    for c in r["two_order"]:print(f'C264 two_order seed={r["seed"]} arm={r["arm"]} metrics={c}')
print("persisted_anchor_deletion_restoration_and_provenance = PASS; protected_inputs = preserved")
print("C263_verdict_unchanged; learning_rate_benefit_claim = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C263Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C264 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C264 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
