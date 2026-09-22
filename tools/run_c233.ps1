param(
    [Parameter(Mandatory=$true)][string]$C232Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c233_core_ablation.py") (Join-Path $Root "tests_lm\test_v05_c233_core_ablation.py")
if ($LASTEXITCODE -ne 0) { throw "C233 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2753 (2754 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; general_language_claim = False; full_retraining_steps = 0"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c233_core_ablation as b
b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 244; protected_inputs = 346", flush=True)
'@
& $Python -u -c $Precheck $C232Summary
if ($LASTEXITCODE -ne 0) { throw "C233 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c233_core_ablation as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 118
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2753
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c233-v5b-core-ablation-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C233 own authoring tests first: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c233_core_ablation -v
    if ($LASTEXITCODE -ne 0) { throw "C233 own tests failed; do not run regression or science" }
    Write-Output "authoring_selftest = PASS"
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C233 regression failed; do not run core ablation" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.model_c233_core_ablation --c232-summary $C232Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C233 execution failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c233_core_ablation as b
out = Path(sys.argv[1])
b.precheck(Path(sys.argv[2]), Path.cwd())
a = b.parent_module().audit_module()
p = a.read_json(out / "summary.json")
b.validate_result(p)
assert p["commit_sha"] == sys.argv[3]
for name, wanted in p["input_sha256"].items():
    assert a.sha(name) == wanted, name
for item in p["artifacts"]:
    path = a.safe_child(out, item["file"])
    assert a.sha(path) == item["sha256"] and path.stat().st_size == item["serialized_bytes"]
rows = a.read_json(out / "comparisons.json")
assert b.summary_for(rows) == p["validation_summary"]
print("=== C233 COMPARISONS; BACKBONE MATCHED, NOT PARAMETER MATCHED ===")
print(json.dumps(rows, ensure_ascii=False, indent=2))
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("scientific_status =", p["status"])
s = p["validation_summary"]
for key in ("baseline_qualified", "full_win_cells", "baseline_win_cells", "tied_cells", "delta_full_minus_baseline_bpb", "all_replays", "total_new_training_steps", "full_retraining_steps"):
    print(key, "=", s[key])
print("interpretation =", "QUALIFIED_COMPARISON" if s["baseline_qualified"] else "INCONCLUSIVE_BASELINE_NOT_QUALIFIED")
print("core_ablation_gate =", b.gate(s))
'@
    & $Python -u -c $Postcheck $Out $C232Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C233 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C233 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
