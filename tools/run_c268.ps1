param(
    [Parameter(Mandatory=$true)][string]$C267Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c268_paired_query_loss.py") (Join-Path $Root "tests_lm\test_v05_c268_paired_query_loss.py")
    if ($LASTEXITCODE -ne 0) { throw "C268 Python syntax preflight failed" }
    Write-Output "expected_focused_tests = 3597 (3598 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 10; training_steps = 8000; model_forwards = 8540; rows = 435840"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c268_paired_query_loss as b
b.precheck(Path(sys.argv[1]),Path.cwd())
parent,*_=b.context()
data=parent.dataset();parent.validate_data(data)
for seed in b.SEEDS:
    indices,profiles,plan=b.schedule(seed,data["TRAIN"])
    assert tuple(indices.shape)==(800,48)
    assert plan["row_exposures"]==[200]*192
    assert plan["profile_updates"]==[268,268,264]
print("source_and_artifact_precheck = PASS; source_pins = 454; protected_inputs = 774",flush=True)
print("both arms use identical paired batches; targets reach loss only",flush=True)
'@
    & $Python -u -c $Precheck $C267Summary
    if ($LASTEXITCODE -ne 0) { throw "C268 parent/task precheck failed" }
    Write-Output "=== C268 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c268_paired_query_loss -v
    if ($LASTEXITCODE -ne 0) { throw "C268 own tests failed; do not run regression or training" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c268_paired_query_loss as b
modules=b.regression_modules(Path.cwd())
assert len(modules)==len(set(modules))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C268 regression failed; do not run training" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c268-v5b-query-loss-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c268_paired_query_loss --c267-summary $C267Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C268 training/evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c268_paired_query_loss as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,metrics=b.verify_artifacts(out,head)
a=b.context()[-1]
print("=== C268 DECIDING METRICS; PAIRED QUERY LOSS ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in metrics:
    print(f'C268 model seed={r["seed"]} arm={r["arm"]} passed={r["passed"]}')
    for c in r["totals"]:print(f'C268 total seed={r["seed"]} arm={r["arm"]} metrics={c}')
    for c in r["cells"]:print(f'C268 cell seed={r["seed"]} arm={r["arm"]} metrics={c}')
    for c in r["two_order"]:print(f'C268 two_order seed={r["seed"]} arm={r["arm"]} metrics={c}')
print("persisted_paired_loss_scores = PASS; protected_inputs = preserved")
print("C267_valid_negative_unchanged; unseen_name_transfer_claim = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C267Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C268 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C268 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
