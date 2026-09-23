param(
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c240_saved_position_audit.py") (Join-Path $Root "tests_lm\test_v05_c240_saved_position_audit.py")
if ($LASTEXITCODE -ne 0) { throw "C240 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2929 (2930 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; saved_prediction_audit_only = True; new_training_steps = 0"
Write-Output "model_forward_calls = 0; saved_predictions = 288; normal_rule_comparisons = 576"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c240_saved_position_audit as b
b.precheck(Path(sys.argv[1]),Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 286; protected_inputs = 430",flush=True)
print("parent_discrete_prediction_metric_replay = PASS; NLL_recomputed = False",flush=True)
'@
& $Python -u -c $Precheck $C239Summary
if ($LASTEXITCODE -ne 0) { throw "C240 source/artifact/prediction precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c240_saved_position_audit as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c240-v5b-saved-position-audit-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C240 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c240_saved_position_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C240 own tests failed; do not run regression or audit" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C240 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C240 regression failed; do not run audit" }
    Confirm-Repository
    Write-Output "=== C240 saved-prediction rule audit ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c240_saved_position_audit --c239-summary $C239Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C240 audit failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c240_saved_position_audit as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,reports=b.verify_artifacts(out,parent,head)
_,_,a=b.context()
print("=== C240 DECIDING DIAGNOSTICS; RECORDED C239 ANSWERS ONLY ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("diagnostic_status =",p["status"])
for key,value in p["validation_summary"].items(): print(key,"=",value)
for r in reports:
    for c in r["cells"]:
        counts=c["categories"];rules=c["rule_matches"]
        print(f'C240 seed={r["seed"]} family={r["family"]} split={c["split"]} lang={c["language"]} '
              f'rows={c["rows"]} correct={counts["correct"]} other_entity={counts["other_entity"]} '
              f'outside_supplied={counts["outside_supplied"]} rule_matches={rules}')
pairs=a.read_json(out/"paired-orders.json")
for seed,family in b.identities():
    for lang in ("en","ja"):
        rows=[r for r in pairs if (r["seed"],r["family"],r["language"])==(seed,family,lang)]
        print(f'C240 paired_order seed={seed} family={family} lang={lang} pairs={len(rows)} '
              f'same_answer={sum(r["same_answer"] for r in rows)} '
              f'both_correct={sum(r["both_correct"] for r in rows)} '
              f'both_fixed_position={sum(r["both_fixed_position"] for r in rows)}')
print("rule_identifiability = TRAIN entity=fixed_position; HOLDOUT fixed_position=other_entity")
print("persisted_saved_answer_audit_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C239Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C240 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C240 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
