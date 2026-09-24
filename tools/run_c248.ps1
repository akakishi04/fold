param(
    [Parameter(Mandatory=$true)][string]$C247Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c248_residual_token_read.py") (Join-Path $Root "tests_lm\test_v05_c248_residual_token_read.py")
if ($LASTEXITCODE -ne 0) { throw "C248 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3121 (3122 loaded -1 inherited exclusion)"
Write-Output "Gate_F = NOT_PASSED; production_adoption = False; two_arms = True"
Write-Output "models = 12; added_parameters_per_arm = 768; train_steps = 4800"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c248_residual_token_read as b
b.precheck(Path(sys.argv[1]),Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 334; protected_inputs = 526",flush=True)
print("C244_optimizer_and_row_schedule = PASS; reader_vs_equal_parameter_EOS_adapter",flush=True)
'@
& $Python -u -c $Precheck $C247Summary
if ($LASTEXITCODE -ne 0) { throw "C248 parent/precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c248_residual_token_read as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c248-v5b-residual-token-read-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C248 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c248_residual_token_read -v
    if ($LASTEXITCODE -ne 0) { throw "C248 own tests failed; stop before regression or pilot" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C248 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C248 regression failed; stop before pilot" }
    Confirm-Repository
    Write-Output "=== C248 paired residual readout pilot ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c248_residual_token_read --c247-summary $C247Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C248 pilot failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c248_residual_token_read as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,records=b.verify_artifacts(out,parent,head)
_,_,_,_,_,a=b.context()
print("=== C248 DECIDING METRICS; READER / EQUAL-PARAMETER EOS CONTROL ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for key,value in p["validation_summary"].items():print(key,"=",value)
for r in records:
    for split in b.SPLITS:
        for lang,m in r["final"][split].items():
            print(f'C248 seed={r["seed"]} family={r["family"]} arm={r["arm"]} split={split} lang={lang} '
                f'accuracy={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
                f'query_pair={m["query_pair_accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f}')
print("persisted_readout_pair_and_discrete_replay = PASS; protected_inputs = preserved")
print("production_adoption = False; no_Gate_F_or_general_language_promotion")
'@
    & $Python -u -c $Postcheck $Out $C247Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C248 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C248 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
