param(
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c237_frozen_signal_audit.py") (Join-Path $Root "tests_lm\test_v05_c237_frozen_signal_audit.py")
if ($LASTEXITCODE -ne 0) { throw "C237 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2857 (2858 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; diagnostic_only = True; new_training_steps = 0"
Write-Output "expected_model_forward_calls = 36; expected_row_presentations = 576"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c237_frozen_signal_audit as b
b.precheck(Path(sys.argv[1]),Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 268; protected_inputs = 394",flush=True)
'@
& $Python -u -c $Precheck $C236Summary
if ($LASTEXITCODE -ne 0) { throw "C237 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c237_frozen_signal_audit as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c237-v5b-frozen-signal-audit-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C237 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c237_frozen_signal_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C237 own tests failed; do not run regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C237 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C237 regression failed; do not run diagnostic" }
    Confirm-Repository
    Write-Output "=== C237 frozen signal audit ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c237_frozen_signal_audit --c236-summary $C236Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C237 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c237_frozen_signal_audit as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,rows=b.verify_artifacts(out,parent,head)
_,_,_,a=b.context()
print("=== C237 DECIDING DIAGNOSTICS; FROZEN C236 MODELS ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("diagnostic_status =",p["status"])
for key,value in p["validation_summary"].items(): print(key,"=",value)
for row in rows:
    for lang,cell in row["cells"].items():
        for kind,stat in cell.items():
            layers=stat["layers"]
            print(f'C237 seed={row["seed"]} family={row["family"]} lang={lang} kind={kind} '
                f'count={stat["count"]} token_equal={stat["input_equal"]} same_answer={stat["same_answer"]} '
                f'both_correct={stat["both_correct"]} '
                f'gru_exact_equal={layers["gru_eos"]["exact_equal"]} '
                f'gru_linf_min={layers["gru_eos"]["linf_min"]:.12g} gru_linf_max={layers["gru_eos"]["linf_max"]:.12g} '
                f'pooled_linf_max={layers["pooled"]["linf_max"]:.12g} '
                f'readout_linf_max={layers["readout"]["linf_max"]:.12g} '
                f'logit_linf_max={layers["logits"]["linf_max"]:.12g} '
                f'digit_margin_change_max={stat["digit_margin_change_max"]:.12g}')
print("persisted_trace_contrast_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C236Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C237 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C237 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
