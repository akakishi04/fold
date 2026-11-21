param(
    [Parameter(Mandatory=$true)][string]$C264Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c265_compound_identifiers.py") (Join-Path $Root "tests_lm\test_v05_c265_compound_identifiers.py")
    if ($LASTEXITCODE -ne 0) { throw "C265 Python syntax preflight failed" }
    Write-Output "expected_focused_tests = 3525 (3526 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 20; new_training = 0; model_forwards = 600; rows = 86400"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c265_compound_identifiers as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 436; protected_inputs = 736",flush=True)
print("identifier_dataset_sha256 =",b.DATA_SHA,flush=True)
print("profiles =",b.PROFILES,"; rows_per_profile = 288; new_training = 0",flush=True)
'@
    & $Python -u -c $Precheck $C264Summary $C263Summary
    if ($LASTEXITCODE -ne 0) { throw "C265 parent/task precheck failed" }
    Write-Output "=== C265 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c265_compound_identifiers -v
    if ($LASTEXITCODE -ne 0) { throw "C265 own tests failed; do not run regression or evaluation" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c265_compound_identifiers as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C265 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C265 regression failed; do not run evaluation" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c265-v5b-identifiers-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C265 frozen identifier evaluation; no training ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c265_compound_identifiers --c264-summary $C264Summary --c263-summary $C263Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C265 evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c265_compound_identifiers as b
out,p264,p263,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
b.precheck(p264,p263,Path.cwd())
p,metrics=b.verify_artifacts(out,p264,p263,head)
a=b.context()[-1]
print("=== C265 DECIDING METRICS; FROZEN COMPOUND IDENTIFIERS ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in metrics:
    for profile,m in r["profiles"].items():
        print(f'C265 model seed={r["seed"]} arm={r["arm"]} profile={profile} correct={m["correct"]}/{m["rows"]} passed={m["passed"]}')
        for c in m["cells"]:print(f'C265 cell seed={r["seed"]} arm={r["arm"]} profile={profile} metrics={c}')
        for c in m["two_order"]:print(f'C265 two_order seed={r["seed"]} arm={r["arm"]} profile={profile} metrics={c}')
print("persisted_identifier_scores_and_anchor_restoration = PASS; protected_inputs = preserved")
print("C264_verdict_unchanged; arbitrary_name_claim = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C264Summary $C263Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C265 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C265 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
