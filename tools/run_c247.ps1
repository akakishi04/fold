param(
    [Parameter(Mandatory=$true)][string]$C246Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c247_normal_exposure_control.py") (Join-Path $Root "tests_lm\test_v05_c247_normal_exposure_control.py")
if ($LASTEXITCODE -ne 0) { throw "C247 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3097 (3098 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; PRIMARY = TRAIN_EXPOSURE_SUFFICIENCY; HOLDOUT = SECONDARY"
Write-Output "train_steps = 1200; normal_presentations = 38400; masked_updates = 0"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c247_normal_exposure_control as b
b.precheck(Path(sys.argv[1]),Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 328; protected_inputs = 514",flush=True)
print("C246_normal_subsequence_and_optimizer_AST = PASS; updates_per_model = 200",flush=True)
'@
& $Python -u -c $Precheck $C246Summary
if ($LASTEXITCODE -ne 0) { throw "C247 parent/control precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c247_normal_exposure_control as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c247-v5b-normal-exposure-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C247 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c247_normal_exposure_control -v
    if ($LASTEXITCODE -ne 0) { throw "C247 own tests failed; do not run regression or control" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C247 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C247 regression failed; do not run control" }
    Confirm-Repository
    Write-Output "=== C247 fresh normal-exposure control ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c247_normal_exposure_control --c246-summary $C246Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C247 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c247_normal_exposure_control as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,records=b.verify_artifacts(out,parent,head)
_,_,_,_,_,a=b.context()
print("=== C247 DECIDING METRICS; TRAIN SUFFICIENCY PRIMARY / HOLDOUT SECONDARY ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for key,value in p["validation_summary"].items():print(key,"=",value)
for r in records:
    for split in b.SPLITS:
        for lang,m in r["final"][split].items():
            c246=r["c246_comparator"][split][lang]
            c244=r["c244_comparator"][split][lang]
            print(f'C247 seed={r["seed"]} family={r["family"]} split={split} lang={lang} '
                f'accuracy={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
                f'query_pair={m["query_pair_accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} '
                f'answer_nll={m["answer_nll"]:.6f} C246_accuracy={c246["accuracy"]:.6f} '
                f'delta_vs_C246={m["accuracy"]-c246["accuracy"]:.6f} C244_accuracy={c244["accuracy"]:.6f}')
print("persisted_control_comparator_and_discrete_replay = PASS; protected_inputs = preserved")
print("primary_PASS_is_TRAIN_control_only; not_a_Gate_F_or_generalization_claim")
'@
    & $Python -u -c $Postcheck $Out $C246Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C247 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C247 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
