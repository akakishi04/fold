param(
    [Parameter(Mandatory=$true)][string]$C241Summary,
    [Parameter(Mandatory=$true)][string]$C234Dataset,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c242_balanced_recombination.py") (Join-Path $Root "tests_lm\test_v05_c242_balanced_recombination.py")
if ($LASTEXITCODE -ne 0) { throw "C242 Python syntax failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2977 (2978 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; TRAIN32; HOLDOUT64; training_steps = 2400"
Write-Output "expected_model_forward_calls = 2490; expected_row_presentations = 80832"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c242_balanced_recombination as b
parent,data=Path(sys.argv[1]),Path(sys.argv[2])
b.precheck(parent,data,Path.cwd())
parts,_=b.load_inputs(parent,data)
print("source_and_artifact_precheck = PASS; source_pins = 298; protected_inputs = 454",flush=True)
print("data_shortcut_audit = PASS; evidence_blind_ceiling = 0.25; query_only_ceiling = 0.25; fixed_position = 0.50",flush=True)
print("partition_rows =",{k:len(v) for k,v in parts.items()},flush=True)
'@
& $Python -u -c $Precheck $C241Summary $C234Dataset
if ($LASTEXITCODE -ne 0) { throw "C242 parent/data/shortcut precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c242_balanced_recombination as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c242-v5b-balanced-recombination-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C242 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c242_balanced_recombination -v
    if ($LASTEXITCODE -ne 0) { throw "C242 own tests failed; do not run regression or probe" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C242 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C242 regression failed; do not run probe" }
    Confirm-Repository
    Write-Output "=== C242 fresh balanced recombination probe ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c242_balanced_recombination --c241-summary $C241Summary --c234-dataset $C234Dataset --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C242 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c242_balanced_recombination as b
out,parent,data,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
b.precheck(parent,data,Path.cwd())
p,rows=b.verify_artifacts(out,parent,data,head)
_,_,_,a=b.context()
print("=== C242 DECIDING METRICS; BALANCED TRAIN32 / RECOMBINATION HOLDOUT64 ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items(): print(k,"=",v)
for r in rows:
    for split in b.SPLITS:
        for lang,m in r["final"][split].items():
            print(f'C242 seed={r["seed"]} family={r["family"]} split={split} lang={lang} '
                f'rows={m["rows"]} accuracy={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
                f'query_pair={m["query_pair_accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f}')
print("persisted_split_initial_identity_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C241Summary $C234Dataset $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C242 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C242 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
