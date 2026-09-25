param(
    [Parameter(Mandatory=$true)][string]$C258Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c259_order_coverage_training.py") (Join-Path $Root "tests_lm\test_v05_c259_order_coverage_training.py")
    if ($LASTEXITCODE -ne 0) { throw "C259 Python syntax preflight failed" }
    Write-Output "python_syntax_preflight = PASS"
    Write-Output "expected_focused_tests = 3381 (3382 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 10; training_steps = 8000; model_forwards = 8240; rows = 435840"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c259_order_coverage_training as b
b.precheck(Path(sys.argv[1]),Path.cwd())
_,base,orders,_,_,factory,_=b.context()
parts=base.dataset();extra=orders.novel_dataset(parts)
assert b.digest(parts)==b.manifest()["original_dataset_sha256"]
assert b.digest(extra)==b.manifest()["extra_dataset_sha256"]
x,y=b.training_tables(parts,factory,orders)
print("source_and_artifact_precheck = PASS; source_pins = 400; protected_inputs = 659",flush=True)
print("paired_training_tables =",tuple(x.shape),"targets =",tuple(y.shape),"seeds =",b.SEEDS,flush=True)
'@
    & $Python -u -c $Precheck $C258Summary
    if ($LASTEXITCODE -ne 0) { throw "C259 parent/task precheck failed" }
    Write-Output "=== C259 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c259_order_coverage_training -v
    if ($LASTEXITCODE -ne 0) { throw "C259 own tests failed; do not run regression or training" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c259_order_coverage_training as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C259 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C259 regression failed; do not run training" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c259-v5b-order-coverage-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C259 paired order-coverage training ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c259_order_coverage_training --c258-summary $C258Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C259 training/evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c259_order_coverage_training as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,measurements=b.verify_artifacts(out,head)
a=b.context()[6]
print("=== C259 DECIDING METRICS; PAIRED ORDER-COVERAGE TRAINING ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in measurements:
    for split in b.SPLITS:
        for lang,m in r["original"][split].items():
            print(f'C259 original seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} metrics={m}')
        for c in r["extra_orders"][split]:
            print(f'C259 extra seed={r["seed"]} arm={r["arm"]} split={split} metrics={c}')
        for lang,m in r["six_order"][split].items():
            print(f'C259 all_orders seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} six={m} accuracy={r["all_order_accuracy"][split][lang]}')
print("persisted_final_logits_and_metrics_recomputation = PASS; protected_inputs = preserved")
print("C256_C257_C258_verdicts_unchanged; unseen_order_transfer_claim = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C258Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C259 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C259 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
