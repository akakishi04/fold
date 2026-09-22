param(
    [Parameter(Mandatory=$true)][string]$C217Summary,
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
    if ($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss") {
        throw "Unexpected branch: $branch"
    }
    $head = git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead) {
        throw "Unexpected HEAD: $head"
    }
    $dirty = @(git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) {
        throw "Tracked tree must be clean"
    }
}

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Authoritative Python missing"
}
Confirm-Repository

Write-Output "=== C218 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05\memory_writer.py") (Join-Path $Root "fold_lm\v05_benchmarks\gate_f_c218_learned_writer.py") (Join-Path $Root "tests_lm\test_v05_c218_learned_writer.py")
if ($LASTEXITCODE -ne 0) {
    throw "C218 Python syntax preflight failed"
}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C218 V5-F learned semantic Writer pilot ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed condition = learned factor+relation Writer only; operation kind oracle; accepted Selector/Readers frozen"
Write-Output "expected_focused_tests = 2259 (2260 loaded -1 exact mutable historical test); Gate_F = NOT_PASSED"

$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c218_learned_writer as b
b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS; accepted C217 checkpoint fixed", flush=True)
'@
& $Python -u -c $Precheck $C217Summary
if ($LASTEXITCODE -ne 0) {
    throw "C218 source/artifact precheck failed"
}

$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import gate_f_c218_learned_writer as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 103
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2259, f"Expected 2259 tests, got {suite.countTestCases()}"
r = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out = Join-Path $Root ("runs\c218-v5f-learned-writer-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed = $false

try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) {
        throw "C218 regression failed; do not run learned Writer pilot"
    }
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_f_c218_learned_writer --c217-summary $C217Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) {
        throw "C218 execution failed"
    }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c218_learned_writer as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out = Path(sys.argv[1])
b.precheck(Path(sys.argv[2]), Path.cwd())
p = audit.read_json(out / "summary.json")
b.validate_result(p)
assert p["commit_sha"] == sys.argv[3]
for name, want in p["input_sha256"].items():
    assert audit.sha(name) == want, name
for a in p["artifacts"]:
    f = audit.safe_child(out, a["file"])
    assert audit.sha(f) == a["sha256"] and f.stat().st_size == a["serialized_bytes"], str(f)
s = p["validation_summary"]
print("summary =", out / "summary.json")
print("summary_sha256 =", audit.sha(out / "summary.json"))
print("scientific_status =", p["status"])
print("seed_relation =", [(r["seed"], r["eval_relation_accuracy"]) for r in s["writer_seed_records"]])
print("seed_assert =", [(r["seed"], r["assert_metrics"]["accuracy"]) for r in s["writer_seed_records"]])
print("seed_replace =", [(r["seed"], r["replace_metrics"]["accuracy"]) for r in s["writer_seed_records"]])
print("wrong_semantic =", s["wrong_semantic_control"]["accuracy"])
print("wrong_factor =", s["wrong_factor_control"]["accuracy"])
print("writer_gate =", b.gate(s))
'@
    & $Python -u -c $Postcheck $Out $C217Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) {
        throw "C218 artifact postcheck failed"
    }
    $Completed = $true
}
finally {
    Write-Output "=== C218 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
