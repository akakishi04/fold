param(
    [Parameter(Mandatory=$true)][string]$C219Summary,
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
    if ($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss") { throw "Unexpected branch: $branch" }
    $head = git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead) { throw "Unexpected HEAD: $head" }
    $dirty = @(git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { throw "Tracked tree must be clean" }
}

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Authoritative Python missing" }
Confirm-Repository

Write-Output "=== C220 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05\memory_stack.py") (Join-Path $Root "fold_lm\v05_benchmarks\gate_f_c220_frozen_learned_stack.py") (Join-Path $Root "tests_lm\test_v05_c220_frozen_learned_stack.py")
if ($LASTEXITCODE -ne 0) { throw "C220 Python syntax preflight failed" }
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C220 V5-F frozen learned stack integration ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed condition = compose frozen learned Writer/Coverage/Selector/Reader; no new training"
Write-Output "expected_focused_tests = 2335 (2336 loaded -1 exact mutable historical test); Gate_F = NOT_PASSED"

$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c220_frozen_learned_stack as b
b.precheck(Path(sys.argv[1]), Path.cwd())
print("source_and_artifact_precheck = PASS; accepted C219 checkpoint fixed", flush=True)
'@
& $Python -u -c $Precheck $C219Summary
if ($LASTEXITCODE -ne 0) { throw "C220 source/artifact precheck failed" }

$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import gate_f_c220_frozen_learned_stack as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == 105
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == 2335, f"Expected 2335 tests, got {suite.countTestCases()}"
r = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out = Join-Path $Root ("runs\c220-v5f-frozen-learned-stack-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed = $false

try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C220 regression failed; do not run frozen-stack integration" }
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_f_c220_frozen_learned_stack --c219-summary $C219Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C220 execution failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c220_frozen_learned_stack as b
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
print("checkpoint_combinations =", s["checkpoint_combinations"])
print("decision_rows =", s["decision_rows"])
print("integration_accuracy =", s["integration_accuracy"])
print("readable_answer_accuracy =", s["readable_answer_accuracy"])
print("nonreadable_suppression_accuracy =", s["nonreadable_suppression_accuracy"])
print("missing_oos_confusions =", s["missing_oos_confusions"])
print("placement_mismatches =", s["placement_mismatches"])
print("stack_gate =", b.gate(s))
'@
    & $Python -u -c $Postcheck $Out $C219Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C220 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C220 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
