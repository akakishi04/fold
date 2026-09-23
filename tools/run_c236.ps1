param(
    [Parameter(Mandatory=$true)][string]$C235Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c236_minimal_binding.py") (Join-Path $Root "tests_lm\test_v05_c236_minimal_binding.py")
if ($LASTEXITCODE -ne 0) { throw "C236 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 2833 (2834 loaded -1 registered historical exclusion)"
Write-Output "Gate_F = NOT_PASSED; minimal_TRAIN_probe_only = True; training_steps = 2400"
Write-Output "expected_model_forward_calls = 2454; expected_total_row_presentations = 77664"

$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c236_minimal_binding as b
b.precheck(Path(sys.argv[1]), Path(sys.argv[2]), Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 262; protected_inputs = 382", flush=True)
print("C234_training_algorithm_AST_parity = PASS", flush=True)
'@
& $Python -u -c $Precheck $C235Summary $C234Summary
if ($LASTEXITCODE -ne 0) { throw "C236 source/artifact/training-contract precheck failed" }

$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c236_minimal_binding as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c236-v5b-minimal-binding-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C236 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c236_minimal_binding -v
    if ($LASTEXITCODE -ne 0) { throw "C236 own tests failed; do not run regression or probe" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C236 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C236 regression failed; do not run probe" }
    Confirm-Repository
    Write-Output "=== C236 minimal TRAIN binding probe ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c236_minimal_binding --c235-summary $C235Summary --c234-summary $C234Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C236 execution failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c236_minimal_binding as b
out = Path(sys.argv[1])
c235 = Path(sys.argv[2])
c234 = Path(sys.argv[3])
expected_head = sys.argv[4]
_, _, _, a = b.context()
b.precheck(c235, c234, Path.cwd())
p = a.read_json(out / "summary.json")
b.validate_result(p)
assert p["commit_sha"] == expected_head
for name, wanted in p["input_sha256"].items():
    assert a.sha(name) == wanted, name
for item in p["artifacts"]:
    path = a.safe_child(out, item["file"])
    assert a.sha(path) == item["sha256"]
    assert path.stat().st_size == item["serialized_bytes"]
rows = a.read_json(out / "measurements.json")
assert b.summarize(rows) == p["validation_summary"]
assert b.digest(a.read_json(out / "probe-dataset.json")) == b.PROBE_SHA
print("=== C236 DECIDING METRICS; SEEN TRAIN16 ONLY ===")
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("scientific_status =", p["status"])
for key, value in p["validation_summary"].items():
    print(key, "=", value)
for row in rows:
    for lang in ("en", "ja"):
        m = row["final_probe"][lang]
        print(f'C236 seed={row["seed"]} family={row["family"]} lang={lang} '
              f'probe_acc={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
              f'query_pair={m["query_pair_accuracy"]:.6f} '
              f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} '
              f'answer_nll={m["answer_nll"]:.6f}')
'@
    & $Python -u -c $Postcheck $Out $C235Summary $C234Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C236 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C236 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
