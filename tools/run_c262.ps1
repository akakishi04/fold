param(
    [Parameter(Mandatory=$true)][string]$C261Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c262_minibatch_order.py") (Join-Path $Root "tests_lm\test_v05_c262_minibatch_order.py")
    if ($LASTEXITCODE -ne 0) { throw "C262 Python syntax preflight failed" }
    Write-Output "python_syntax_preflight = PASS"
    Write-Output "expected_focused_tests = 3453 (3454 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 10; training_steps = 8000; model_forwards = 8240; rows = 435840"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c262_minibatch_order as b
b.precheck(Path(sys.argv[1]),Path.cwd())
_,_,trainer,base,orders,_,_,factory,_=b.context()
parts=base.dataset();extra=orders.novel_dataset(parts)
assert b.digest(parts)==b.manifest()["original_dataset_sha256"]
assert b.digest(extra)==b.manifest()["extra_dataset_sha256"]
x,y=trainer.training_tables(parts,factory,orders)
assert tuple(x.shape)==(3,144,48) and tuple(y.shape)==(144,)
for seed in b.SEEDS:
    a,c=[b.schedule(seed,arm)[2] for arm in b.ARMS]
    assert a["exposure_counts"]==c["exposure_counts"]
    assert a["chronology_sha256"]!=c["chronology_sha256"]
print("source_and_artifact_precheck = PASS; source_pins = 418; protected_inputs = 697",flush=True)
print("paired_prompt_exposures = identical; minibatch_chronology = different",flush=True)
'@
    & $Python -u -c $Precheck $C261Summary
    if ($LASTEXITCODE -ne 0) { throw "C262 parent/task precheck failed" }
    Write-Output "=== C262 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c262_minibatch_order -v
    if ($LASTEXITCODE -ne 0) { throw "C262 own tests failed; do not run regression or training" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c262_minibatch_order as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C262 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C262 regression failed; do not run training" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c262-v5b-batch-order-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C262 paired minibatch chronology training ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c262_minibatch_order --c261-summary $C261Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C262 training/evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c262_minibatch_order as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,measurements=b.verify_artifacts(out,head)
a=b.context()[-1]
print("=== C262 DECIDING METRICS; PAIRED MINIBATCH CHRONOLOGY ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in measurements:
    print(f'C262 seed={r["seed"]} arm={r["arm"]} passed={r["passed"]} outcome={r["outcome"]}')
    for split in b.SPLITS:
        for lang,m in r["original"][split].items():
            print(f'C262 original seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} metrics={m}')
        for m in r["extra_orders"][split]:
            print(f'C262 extra seed={r["seed"]} arm={r["arm"]} split={split} metrics={m}')
        for lang,m in r["six_order"][split].items():
            print(f'C262 all_orders seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} six={m} accuracy={r["all_order_accuracy"][split][lang]}')
print("persisted_scores_schedules_and_answer_flips = PASS; protected_inputs = preserved")
print("C261_valid_negative_unchanged; production_adoption = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C261Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C262 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C262 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
