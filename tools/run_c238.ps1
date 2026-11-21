param(
    [Parameter(Mandatory=$true)][string]$C237Summary,
    [Parameter(Mandatory=$true)][string]$C236Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c238_complete_cohort_sampler.py") (Join-Path $Root "tests_lm\test_v05_c238_complete_cohort_sampler.py")
if ($LASTEXITCODE -ne 0) { throw "C238 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2881 (2882 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; minimal_TRAIN_probe_only = True; training_steps = 2400"
Write-Output "expected_model_forward_calls = 2454; expected_total_row_presentations = 77664"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c238_complete_cohort_sampler as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 274; protected_inputs = 406",flush=True)
print("training_AST_delta = sampler_only; fixed_batch = every row twice",flush=True)
'@
& $Python -u -c $Precheck $C237Summary $C236Summary
if ($LASTEXITCODE -ne 0) { throw "C238 source/artifact/sampler precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c238_complete_cohort_sampler as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c238-v5b-complete-cohort-sampler-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C238 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c238_complete_cohort_sampler -v
    if ($LASTEXITCODE -ne 0) { throw "C238 own tests failed; do not run regression or probe" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C238 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C238 regression failed; do not run probe" }
    Confirm-Repository
    Write-Output "=== C238 complete-cohort sampler probe ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c238_complete_cohort_sampler --c237-summary $C237Summary --c236-summary $C236Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C238 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c238_complete_cohort_sampler as b
out=Path(sys.argv[1])
c237=Path(sys.argv[2])
c236=Path(sys.argv[3])
head=sys.argv[4]
b.precheck(c237,c236,Path.cwd())
p,rows=b.verify_artifacts(out,c236,head)
_,_,_,_,a=b.context()
print("=== C238 DECIDING METRICS; SAME TRAIN16, SAMPLER CHANGE ONLY ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for key,value in p["validation_summary"].items(): print(key,"=",value)
for row in rows:
    for lang in ("en","ja"):
        m=row["final_probe"][lang]
        old=row["comparator_final"][lang]
        print(f'C238 seed={row["seed"]} family={row["family"]} lang={lang} '
            f'probe_acc={m["accuracy"]:.6f} C236_acc={old["accuracy"]:.6f} '
            f'accuracy_delta={m["accuracy"]-old["accuracy"]:.6f} '
            f'fact_pair={m["fact_pair_accuracy"]:.6f} query_pair={m["query_pair_accuracy"]:.6f} '
            f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} '
            f'answer_nll={m["answer_nll"]:.6f}')
print("persisted_measurement_comparator_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C237Summary $C236Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C238 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C238 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
