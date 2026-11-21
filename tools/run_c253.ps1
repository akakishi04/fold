param(
    [Parameter(Mandatory=$true)][string]$C252Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c253_frozen_residual_path.py") (Join-Path $Root "tests_lm\test_v05_c253_frozen_residual_path.py")
if ($LASTEXITCODE -ne 0) { throw "C253 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3241 (3242 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; frozen_models = 5; training_steps = 0; model_forward_calls = 120; row_presentations = 5760"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c253_frozen_residual_path as b
b.precheck(Path(sys.argv[1]),Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 364; protected_inputs = 587",flush=True)
print("frozen_C252; intact -> pre_residual -> reader_only -> restored; diagnostic_integrity_gate_only",flush=True)
'@
& $Python -u -c $Precheck $C252Summary
if ($LASTEXITCODE -ne 0) { throw "C253 parent/source precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c253_frozen_residual_path as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c253-v5b-frozen-residual-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C253 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c253_frozen_residual_path -v
    if ($LASTEXITCODE -ne 0) { throw "C253 own tests failed; do not run regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C253 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C253 regression failed; do not run diagnostic" }
    Confirm-Repository
    Write-Output "=== C253 frozen residual-path diagnostic ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c253_frozen_residual_path --c252-summary $C252Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C253 diagnostic execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c253_frozen_residual_path as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,diagnostics,contrasts=b.verify_artifacts(out,parent,head)
_,_,_,_,_,a=b.context()
print("=== C253 DECIDING DIAGNOSTICS; FROZEN POST-CORE RESIDUAL ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("diagnostic_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in diagnostics:
    for mode in b.MODES:
        for split in b.SPLITS:
            for lang,m in r["metrics"][mode][split].items():
                print(f'C253 seed={r["seed"]} mode={mode} split={split} lang={lang} '
                      f'accuracy={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
                      f'query_pair={m["query_pair_accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                      f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f}')
for c in contrasts:
    print("C253 contrast =",c)
print("persisted_residual_outputs_and_component_replay = PASS; protected_inputs = preserved")
print("C252_verdict_unchanged; frozen_intervention_not_retraining; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C252Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C253 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C253 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
