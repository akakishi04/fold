param(
    [Parameter(Mandatory=$true)][string]$C240Summary,
    [Parameter(Mandatory=$true)][string]$C239Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c241_assignment_holdout.py") (Join-Path $Root "tests_lm\test_v05_c241_assignment_holdout.py")
if ($LASTEXITCODE -ne 0) { throw "C241 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2953 (2954 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; TRAIN_assignment01 = 8; HOLDOUT_assignment10 = 8; training_steps = 2400"
Write-Output "expected_model_forward_calls = 2490; expected_total_row_presentations = 77520"

$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c241_assignment_holdout as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
parts,_=b.load_inputs(Path(sys.argv[2]))
assert len(parts["TRAIN"])==len(parts["HOLDOUT"])==8
assert {r["order"] for r in parts["TRAIN"]}=={0,1}
assert {r["order"] for r in parts["HOLDOUT"]}=={0,1}
print("source_and_artifact_precheck = PASS; source_pins = 292; protected_inputs = 442",flush=True)
print("position_shortcut_broken_in_TRAIN = PASS; assignment_holdout_disjoint = PASS",flush=True)
'@
& $Python -u -c $Precheck $C240Summary $C239Summary
if ($LASTEXITCODE -ne 0) { throw "C241 source/artifact/split precheck failed" }

$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c241_assignment_holdout as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@

$Out = Join-Path $Root ("runs\c241-v5b-assignment-holdout-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C241 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c241_assignment_holdout -v
    if ($LASTEXITCODE -ne 0) { throw "C241 own tests failed; do not run regression or probe" }
    Write-Output "authoring_selftest = PASS"

    Write-Output "=== C241 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C241 regression failed; do not run probe" }

    Confirm-Repository
    Write-Output "=== C241 fresh assignment-holdout probe ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c241_assignment_holdout --c240-summary $C240Summary --c239-summary $C239Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C241 execution failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c241_assignment_holdout as b
out,c240,c239,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
b.precheck(c240,c239,Path.cwd())
p,rows=b.verify_artifacts(out,c239,head)
_,_,_,_,a=b.context()
print("=== C241 DECIDING METRICS; BOTH POSITIONS TRAIN / SWAPPED ASSIGNMENT HOLDOUT ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for key,value in p["validation_summary"].items(): print(key,"=",value)
for row in rows:
    for split in b.SPLITS:
        for lang,m in row["final"][split].items():
            print(f'C241 seed={row["seed"]} family={row["family"]} split={split} lang={lang} '
                f'accuracy={m["accuracy"]:.6f} query_pair={m["query_pair_accuracy"]:.6f} '
                f'order_pair={m["order_pair_accuracy"]:.6f} evidence_drop={m["evidence_drop"]:.6f} '
                f'query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f}')
print("persisted_assignment_partition_initial_identity_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C240Summary $C239Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C241 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C241 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
