param(
    [Parameter(Mandatory=$true)][string]$C234Summary,
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

& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c235_frozen_binding_diagnostic.py") (Join-Path $Root "tests_lm\test_v05_c235_frozen_binding_diagnostic.py")
if ($LASTEXITCODE -ne 0) { throw "C235 Python syntax preflight failed" }

Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2809 (2810 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; diagnostic_only = True; new_training_steps = 0"
Write-Output "expected_model_forward_calls = 36; expected_evaluated_rows = 10368"

$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c235_frozen_binding_diagnostic as b
b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 256; protected_inputs = 370", flush=True)
'@

& $Python -u -c $Precheck $C234Summary
if ($LASTEXITCODE -ne 0) { throw "C235 source/artifact precheck failed" }

$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c235_frozen_binding_diagnostic as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 120
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2809
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@

$Out = Join-Path $Root ("runs\c235-v5b-frozen-binding-diagnostic-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C235 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c235_frozen_binding_diagnostic -v
    if ($LASTEXITCODE -ne 0) { throw "C235 own tests failed; do not run regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"

    Write-Output "=== C235 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C235 regression failed; do not run diagnostic" }

    Confirm-Repository
    Write-Output "=== C235 frozen diagnostic ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c235_frozen_binding_diagnostic --c234-summary $C234Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C235 execution failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c235_frozen_binding_diagnostic as b

out = Path(sys.argv[1])
parent = Path(sys.argv[2])
expected_head = sys.argv[3]
pmod = b.parent_module()
a = pmod.parent_module().parent_module().audit_module()

b.precheck(parent, Path.cwd())
p = a.read_json(out / "summary.json")
b.validate_result(p)
assert p["commit_sha"] == expected_head

for name, wanted in p["input_sha256"].items():
    assert a.sha(name) == wanted, name
for item in p["artifacts"]:
    path = a.safe_child(out, item["file"])
    assert a.sha(path) == item["sha256"]
    assert path.stat().st_size == item["serialized_bytes"]

rows = a.read_json(out / "diagnostics.json")
assert b.summarize(rows) == p["validation_summary"]

print("=== C235 DECIDING DIAGNOSTICS; FROZEN C234 MODELS ===")
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
s = p["validation_summary"]
print("diagnostic_status =", p["status"])
print("all_parent_replays =", s["all_parent_replays"])
print("all_fingerprints_unchanged =", s["all_fingerprints_unchanged"])
print("model_forward_calls =", s["model_forward_calls"])
print("evaluated_rows_including_masks =", s["evaluated_rows_including_masks"])
print("diagnosis_counts =", s["diagnosis_counts"])
print("capability_pass_claim =", s["capability_pass_claim"])

for row in rows:
    for lang in ("en", "ja"):
        tr = row["metrics"]["TRAIN"][lang]
        ev = row["metrics"]["EVAL"][lang]
        tb = row["behavior"]["TRAIN"][lang]
        eb = row["behavior"]["EVAL"][lang]
        print(
            f'C235 seed={row["seed"]} family={row["family"]} lang={lang} '
            f'diagnosis={row["diagnosis"][lang]} '
            f'train_acc={tr["accuracy"]:.6f} eval_acc={ev["accuracy"]:.6f} '
            f'train_query_pair={tr["query_pair_accuracy"]:.6f} eval_query_pair={ev["query_pair_accuracy"]:.6f} '
            f'train_supplied={tb["supplied_value_rate"]:.6f} eval_supplied={eb["supplied_value_rate"]:.6f} '
            f'train_query_same={tb["query_same_answer_rate"]:.6f} eval_query_same={eb["query_same_answer_rate"]:.6f} '
            f'train_both_correct={tb["query_both_correct_pairs"]}/{tb["query_pairs"]} '
            f'eval_both_correct={eb["query_both_correct_pairs"]}/{eb["query_pairs"]}'
        )
'@

    & $Python -u -c $Postcheck $Out $C234Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C235 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C235 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
