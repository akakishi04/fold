param(
    [Parameter(Mandatory=$true)][string]$C255Summary,
    [Parameter(Mandatory=$true)][string]$ExpectedHead
)
$ErrorActionPreference="Stop"
$PSNativeCommandUseErrorActionPreference=$false
Set-StrictMode -Version Latest
$Root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python=Join-Path $Root ".venv-py31315\Scripts\python.exe"
function Confirm-Repository {
    $branch=git branch --show-current
    if($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss"){throw "Unexpected branch"}
    $head=git rev-parse HEAD
    if($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead){throw "Unexpected HEAD"}
    $dirty=@(git status --porcelain --untracked-files=no)
    if($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0){throw "Tracked tree must be clean"}
}
if(-not(Test-Path -LiteralPath $Python -PathType Leaf)){throw "Authoritative Python missing"}
Confirm-Repository
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c256_three_entity_task_shift.py") (Join-Path $Root "tests_lm\test_v05_c256_three_entity_task_shift.py")
if($LASTEXITCODE -ne 0){throw "C256 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3313 (3314 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; models = 10; training_steps = 8000; model_forwards = 8120; rows = 401280"
$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c256_three_entity_task_shift as b
b.precheck(Path(sys.argv[1]),Path.cwd())
parts=b.dataset()
print("source_and_artifact_precheck = PASS; source_pins = 382; protected_inputs = 623",flush=True)
print("three_entity_task_sha256 =",b.digest(parts),flush=True)
print("rows =",{k:len(v) for k,v in parts.items()},"seeds =",b.SEEDS,flush=True)
'@
& $Python -u -c $Precheck $C255Summary
if($LASTEXITCODE -ne 0){throw "C256 parent/task precheck failed"}
$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c256_three_entity_task_shift as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out=Join-Path $Root ("runs\c256-v5b-three-entity-" + [guid]::NewGuid().ToString("N"))
$Completed=$false
try {
    Write-Output "=== C256 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c256_three_entity_task_shift -v
    if($LASTEXITCODE -ne 0){throw "C256 own tests failed; do not run regression or training"}
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C256 focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C256 regression failed; do not run training"}
    Confirm-Repository
    Write-Output "=== C256 fresh three-entity task-shift training ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c256_three_entity_task_shift --c255-summary $C255Summary --output-dir $Out --expected-head $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C256 execution failed"}
    $Postcheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c256_three_entity_task_shift as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,records=b.verify_artifacts(out,head)
_,_,_,_,a=b.context()
print("=== C256 DECIDING METRICS; FRESH THREE-ENTITY TASK SHIFT ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in records:
    for split in b.SPLITS:
        for lang,m in r["final"][split].items():
            print(f'C256 seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} '
                  f'accuracy={m["accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                  f'query_triplet={m["query_triplet_accuracy"]:.6f} evidence_drop={m["evidence_drop"]:.6f} '
                  f'query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f}')
print("persisted_three_entity_metrics_and_checkpoint_replay = PASS; protected_inputs = preserved")
print("C255_and_earlier_verdicts_unchanged; production_adoption = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C255Summary $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C256 artifact postcheck failed"}
    $Completed=$true
}
finally {
    Write-Output "=== C256 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
