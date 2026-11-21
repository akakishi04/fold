param(
    [Parameter(Mandatory=$true)][string]$C250Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c251_precore_read.py") (Join-Path $Root "tests_lm\test_v05_c251_precore_read.py")
if ($LASTEXITCODE -ne 0) { throw "C251 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3193 (3194 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; models = 5; train_steps = 2000; model_forward_calls = 2075; row_presentations = 67840"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c251_precore_read as b
b.precheck(Path(sys.argv[1]),Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 352; protected_inputs = 563",flush=True)
print("comparator = immutable C250 Full/token_read; query = postcore; memory = precore",flush=True)
'@
& $Python -u -c $Precheck $C250Summary
if ($LASTEXITCODE -ne 0) { throw "C251 parent/recipe precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c251_precore_read as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c251-v5b-precore-read-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C251 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c251_precore_read -v
    if ($LASTEXITCODE -ne 0) { throw "C251 own tests failed; do not run regression or training" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C251 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C251 regression failed; do not run training" }
    Confirm-Repository
    Write-Output "=== C251 Full pre-core read-memory comparison ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c251_precore_read --c250-summary $C250Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C251 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c251_precore_read as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,records=b.verify_artifacts(out,parent,head)
_,_,_,_,a=b.context()
print("=== C251 DECIDING METRICS; PRECORE MEMORY / POSTCORE QUERY ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in records:
    for split in b.SPLITS:
        for lang,m in r["final"][split].items():
            old=r["c250_comparator"][split][lang]
            print(f'C251 seed={r["seed"]} split={split} lang={lang} accuracy={m["accuracy"]:.6f} '
                f'fact_pair={m["fact_pair_accuracy"]:.6f} query_pair={m["query_pair_accuracy"]:.6f} '
                f'order_pair={m["order_pair_accuracy"]:.6f} evidence_drop={m["evidence_drop"]:.6f} '
                f'query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f} '
                f'C250_accuracy={old["accuracy"]:.6f} delta={m["accuracy"]-old["accuracy"]:.6f}')
print("persisted_precore_comparator_and_discrete_replay = PASS; protected_inputs = preserved")
print("C250_verdict_unchanged; production_adoption = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C250Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C251 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C251 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
