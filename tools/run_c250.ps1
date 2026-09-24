param(
    [Parameter(Mandatory=$true)][string]$C249Summary,
    [Parameter(Mandatory=$true)][string]$C248Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c250_fresh_seed_replication.py") (Join-Path $Root "tests_lm\test_v05_c250_fresh_seed_replication.py")
if ($LASTEXITCODE -ne 0) { throw "C250 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3169 (3170 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; production_adoption = False; new_seed_blocks = 5"
Write-Output "models = 20; train_steps = 8000; model_forward_calls = 8330; row_presentations = 273280"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c250_fresh_seed_replication as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
b.load_inputs(Path(sys.argv[2]))
print("source_and_artifact_precheck = PASS; source_pins = 346; protected_inputs = 550",flush=True)
print("unchanged_C248_recipe = PASS; prospective_seeds =",b.SEEDS,flush=True)
'@
& $Python -u -c $Precheck $C249Summary $C248Summary
if ($LASTEXITCODE -ne 0) { throw "C250 parent/recipe precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c250_fresh_seed_replication as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c250-v5b-fresh-seed-replication-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C250 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c250_fresh_seed_replication -v
    if ($LASTEXITCODE -ne 0) { throw "C250 own tests failed; do not run regression or replication" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C250 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C250 regression failed; do not run replication" }
    Confirm-Repository
    Write-Output "=== C250 paired fresh-seed replication ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c250_fresh_seed_replication --c249-summary $C249Summary --c248-summary $C248Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C250 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c250_fresh_seed_replication as b
out,c249,c248,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
b.precheck(c249,c248,Path.cwd())
p,records=b.verify_artifacts(out,c248,head)
_,_,_,_,_,_,a=b.context()
print("=== C250 DECIDING METRICS; FIVE NEW PAIRED SEEDS ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for key,value in p["validation_summary"].items():print(key,"=",value)
for r in records:
    for split in b.SPLITS:
        for lang,m in r["final"][split].items():
            print(f'C250 seed={r["seed"]} family={r["family"]} arm={r["arm"]} split={split} lang={lang} '
                f'accuracy={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
                f'query_pair={m["query_pair_accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f}')
print("persisted_fresh_seed_pair_and_discrete_replay = PASS; protected_inputs = preserved")
print("C248_verdict_unchanged; new_initializations_not_new_external_task; production_adoption = False")
'@
    & $Python -u -c $Postcheck $Out $C249Summary $C248Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C250 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C250 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
