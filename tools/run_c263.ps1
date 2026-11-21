param(
    [Parameter(Mandatory=$true)][string]$C262Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c263_learning_rate_order.py") (Join-Path $Root "tests_lm\test_v05_c263_learning_rate_order.py")
    if ($LASTEXITCODE -ne 0) { throw "C263 Python syntax preflight failed" }
    Write-Output "python_syntax_preflight = PASS"
    Write-Output "expected_focused_tests = 3477 (3478 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 20; training_steps = 16000; model_forwards = 16480; rows = 871680"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c263_learning_rate_order as b
b.precheck(Path(sys.argv[1]),Path.cwd())
_,_,trainer,base,orders,_,_,factory,_=b.context()
parts=base.dataset();extra=orders.novel_dataset(parts)
assert b.digest(parts)==b.manifest()["original_dataset_sha256"]
assert b.digest(extra)==b.manifest()["extra_dataset_sha256"]
x,y=trainer.training_tables(parts,factory,orders)
assert tuple(x.shape)==(3,144,48) and tuple(y.shape)==(144,)
for seed in b.SEEDS:
    a,c=[b.schedule(seed,order)[2] for order in b.ORDERS]
    assert a["exposure_counts"]==c["exposure_counts"]
    assert a["chronology_sha256"]!=c["chronology_sha256"]
print("source_and_artifact_precheck = PASS; source_pins = 424; protected_inputs = 710",flush=True)
print("rates =",b.RATES,"orders =",b.ORDERS,"models =",len(b.identities()),flush=True)
'@
    & $Python -u -c $Precheck $C262Summary
    if ($LASTEXITCODE -ne 0) { throw "C263 parent/task precheck failed" }
    Write-Output "=== C263 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c263_learning_rate_order -v
    if ($LASTEXITCODE -ne 0) { throw "C263 own tests failed; do not run regression or training" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c263_learning_rate_order as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C263 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C263 regression failed; do not run training" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c263-v5b-rate-order-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C263 learning-rate by minibatch-order training ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c263_learning_rate_order --c262-summary $C262Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C263 training/evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c263_learning_rate_order as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,measurements=b.verify_artifacts(out,head)
a=b.context()[-1]
print("=== C263 DECIDING METRICS; RATE BY ORDER ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in measurements:
    print(f'C263 seed={r["seed"]} arm={r["arm"]} lr={r["lr"]} passed={r["passed"]} outcome={r["outcome"]}')
    for split in b.SPLITS:
        for lang,m in r["original"][split].items():
            print(f'C263 original seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} metrics={m}')
        for m in r["extra_orders"][split]:
            print(f'C263 extra seed={r["seed"]} arm={r["arm"]} split={split} metrics={m}')
        for lang,m in r["six_order"][split].items():
            print(f'C263 all_orders seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} six={m} accuracy={r["all_order_accuracy"][split][lang]}')
print("persisted_rate_order_scores_and_interactions = PASS; protected_inputs = preserved")
print("C262_valid_negative_unchanged; learning_rate_benefit_claim = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C262Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C263 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C263 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
