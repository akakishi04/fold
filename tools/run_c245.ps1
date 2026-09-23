param(
    [Parameter(Mandatory=$true)][string]$C244Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c245_selective_evidence.py") (Join-Path $Root "tests_lm\test_v05_c245_selective_evidence.py")
if ($LASTEXITCODE -ne 0) { throw "C245 Python syntax failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3049 (3050 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; frozen_diagnostic = True; new_training_steps = 0"
Write-Output "expected_model_forward_calls = 60; expected_row_presentations = 2880"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c245_selective_evidence as b
b.precheck(Path(sys.argv[1]), Path.cwd())
b.load_inputs(Path(sys.argv[1]))
print("source_and_artifact_precheck = PASS; source_pins = 316; protected_inputs = 490", flush=True)
print("selective_input_layout_and_ambiguity_precheck = PASS; no_checkpoint_loaded_in_precheck", flush=True)
'@
& $Python -u -c $Precheck $C244Summary
if ($LASTEXITCODE -ne 0) { throw "C245 parent/source/input precheck failed" }
$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c245_selective_evidence as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c245-v5b-selective-evidence-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C245 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c245_selective_evidence -v
    if ($LASTEXITCODE -ne 0) { throw "C245 own tests failed; do not run regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C245 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C245 regression failed; do not run diagnostic" }
    Confirm-Repository
    Write-Output "=== C245 frozen selective-evidence diagnostic ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c245_selective_evidence --c244-summary $C244Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C245 diagnostic failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c245_selective_evidence as b
out, parent, head = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
b.precheck(parent, Path.cwd())
p, cells = b.verify_artifacts(out, parent, head)
_, _, _, _, a = b.context()
print("=== C245 DECIDING DIAGNOSTICS; FROZEN C244 SELECTIVE ERASURE ===")
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("diagnostic_status =", p["status"])
for k, v in p["validation_summary"].items(): print(k, "=", v)
for c in cells:
    for view in ("normal",) + b.SELECTIVE:
        m = c["views"][view]
        print(f'C245 seed={c["seed"]} family={c["family"]} split={c["split"]} lang={c["language"]} '
              f'view={view} rows={c["rows"]} accuracy={m["accuracy"]:.6f} drop={m["accuracy_drop"]:.6f} '
              f'flips={m["answer_flips"]} broken={m["correct_to_wrong"]} repaired={m["wrong_to_correct"]} '
              f'answer_nll={m["answer_nll"]:.6f} nll_increase={m["nll_increase"]:.6f} logit_linf={m["logit_linf"]:.9g}')
print("selective_masks = distribution_shift_and_redundancy_caveats; not_a_capability_gate")
print("persisted_logit_diagnostic_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C244Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C245 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C245 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
