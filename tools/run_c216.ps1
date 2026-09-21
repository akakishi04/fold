param(
    [Parameter(Mandatory=$true)][string]$C215Summary,
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

Write-Output "=== C216 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05\memory_reader.py") (Join-Path $Root "fold_lm\v05_benchmarks\gate_f_c216_learned_reader.py") (Join-Path $Root "tests_lm\test_v05_c216_learned_reader.py")
if ($LASTEXITCODE -ne 0) {
    throw "C216 Python syntax preflight failed"
}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C216 V5-F learned Reader pilot ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed condition = learned Reader only over oracle-selected scalar memory port"
Write-Output "expected_focused_tests = 2185 (2186 loaded -1 exact mutable historical test); Gate_F = NOT_PASSED"

$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as b
b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS; accepted C215 maintenance checkpoint fixed", flush=True)
'@
& $Python -u -c $Precheck $C215Summary
if ($LASTEXITCODE -ne 0) {
    throw "C216 source/artifact precheck failed"
}

$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 101
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2185, f"Expected 2185 tests, got {suite.countTestCases()}"
r = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out = Join-Path $Root ("runs\c216-v5f-learned-reader-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed = $false

try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) {
        throw "C216 regression failed; do not run learned Reader pilot"
    }
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_f_c216_learned_reader --c215-summary $C215Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) {
        throw "C216 execution failed"
    }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as b
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
print("seed_eval =", [(r["seed"], r["eval_accuracy"]) for r in s["seed_records"]])
print("seed_zero =", [(r["seed"], r["zero_readout_eval_accuracy"]) for r in s["seed_records"]])
print("placement_mismatches =", [r["placement_prediction_mismatches"] for r in s["seed_records"]])
print("learned_reader_calls =", s["learned_reader_calls"])
print("reader_gate =", b.gate(s))
'@
    & $Python -u -c $Postcheck $Out $C215Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) {
        throw "C216 artifact postcheck failed"
    }
    $Completed = $true
}
finally {
    Write-Output "=== C216 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
