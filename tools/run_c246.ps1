param(
    [Parameter(Mandatory=$true)][string]$C245Summary,
    [Parameter(Mandatory=$true)][string]$C244Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c246_training_erasure.py") (Join-Path $Root "tests_lm\test_v05_c246_training_erasure.py")
if ($LASTEXITCODE -ne 0) { throw "C246 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3073 (3074 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; TRAIN64/HOLDOUT32 unchanged; normal-only capability endpoint"
Write-Output "train_steps = 2400; answer_presentations = 76800; normal = 38400; masked = 38400"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c246_training_erasure as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
b.load_inputs(Path(sys.argv[2]))
print("source_and_artifact_precheck = PASS; source_pins = 322; protected_inputs = 502",flush=True)
print("row_schedule_and_optimizer_AST_parity = PASS; train_view_cycle = masked,masked,normal,normal",flush=True)
'@
& $Python -u -c $Precheck $C245Summary $C244Summary
if ($LASTEXITCODE -ne 0) { throw "C246 parent/input precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c246_training_erasure as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c246-v5b-training-erasure-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C246 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c246_training_erasure -v
    if ($LASTEXITCODE -ne 0) { throw "C246 own tests failed; do not run regression or training" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C246 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C246 regression failed; do not run training" }
    Confirm-Repository
    Write-Output "=== C246 training-only erasure experiment ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c246_training_erasure --c245-summary $C245Summary --c244-summary $C244Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C246 experiment failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c246_training_erasure as b
out,c245,c244,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
b.precheck(c245,c244,Path.cwd())
p,records=b.verify_artifacts(out,c244,head)
_,_,_,_,_,a=b.context()
print("=== C246 DECIDING METRICS; NORMAL FULL-EVIDENCE ENDPOINT ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for key,value in p["validation_summary"].items():print(key,"=",value)
for r in records:
    print("block_view_updates =",r["seed"],r["family"],r["block_view_updates"])
    for split in b.SPLITS:
        for lang,m in r["final"][split].items():
            old=r["c244_comparator"][split][lang]
            print(f'C246 seed={r["seed"]} family={r["family"]} split={split} lang={lang} '
                f'accuracy={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
                f'query_pair={m["query_pair_accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} '
                f'answer_nll={m["answer_nll"]:.6f} C244_accuracy={old["accuracy"]:.6f} '
                f'delta={m["accuracy"]-old["accuracy"]:.6f}')
print("persisted_normal_endpoint_comparator_and_discrete_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C245Summary $C244Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C246 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C246 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
