param(
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c249_frozen_read_ablation.py") (Join-Path $Root "tests_lm\test_v05_c249_frozen_read_ablation.py")
if ($LASTEXITCODE -ne 0) { throw "C249 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3145 (3146 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; diagnostic_only = True; new_training_steps = 0"
Write-Output "models = 12; model_forward_calls = 180; row_presentations = 8640"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c249_frozen_read_ablation as b
b.precheck(Path(sys.argv[1]),Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 340; protected_inputs = 538",flush=True)
print("checkpoint_source = accepted C248 final states; no new training",flush=True)
'@
& $Python -u -c $Precheck $C248Summary
if ($LASTEXITCODE -ne 0) { throw "C249 parent precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c249_frozen_read_ablation as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c249-v5b-frozen-read-ablation-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C249 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c249_frozen_read_ablation -v
    if ($LASTEXITCODE -ne 0) { throw "C249 own tests failed; stop before regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C249 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C249 regression failed; stop before diagnostic" }
    Confirm-Repository
    Write-Output "=== C249 frozen read-path ablation ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c249_frozen_read_ablation --c248-summary $C248Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C249 diagnostic failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c249_frozen_read_ablation as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,effects=b.verify_artifacts(out,parent,head)
_,_,_,_,_,a=b.context()
print("=== C249 DECIDING DIAGNOSTICS; FROZEN INTACT / OFF / UNIFORM ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("diagnostic_status =",p["status"])
for key,value in p["validation_summary"].items():print(key,"=",value)
for record in effects:
    for mode,data in record["contrasts"].items():
        for split,cell in data.items():
            for lang,m in cell.items():
                print(f'C249 seed={record["seed"]} family={record["family"]} arm={record["arm"]} '
                    f'mode={mode} split={split} lang={lang} intact_accuracy={m["intact"]["accuracy"]:.6f} '
                    f'ablated_accuracy={m["ablated"]["accuracy"]:.6f} accuracy_drop={m["accuracy_drop"]:.6f} '
                    f'answer_flips={m["answer_flips"]} lost_correct={m["lost_correct"]} gained_correct={m["gained_correct"]} '
                    f'nll_change={m["nll_change"]:.6f} max_logit_change={m["max_logit_change"]:.12g}')
print("persisted_ablation_logits_and_contrasts_replay = PASS; protected_inputs = preserved")
print("C248_verdict_unchanged; production_adoption = False")
'@
    & $Python -u -c $Postcheck $Out $C248Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C249 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C249 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
