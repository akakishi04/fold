param(
    [Parameter(Mandatory=$true)][ValidateCount(8,8)][string[]]$Summaries,
    [Parameter(Mandatory=$true)][string]$ExpectedHead,
    [Parameter(Mandatory=$true)][ValidateSet("Validate","Execute")][string]$Mode
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
if ($Mode -eq "Validate") {
    Write-Output "=== C282 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c282_mixed_length_training.py") (Join-Path $Root "tests_lm\test_v05_c282_mixed_length_training.py")
    if ($LASTEXITCODE -ne 0) { throw "C282 Python syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c282_mixed_length_training as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 8
b.precheck(paths, Path.cwd())
c = b.context()
data = c.p267.dataset()
tokens, targets = b.training_tables(data, c)
for seed in b.SEEDS:
    left = b.schedule(seed, b.ARMS[0], data["TRAIN"])
    right = b.schedule(seed, b.ARMS[1], data["TRAIN"])
    assert left[3]["logical_batch_sha256"] == right[3]["logical_batch_sha256"]
    models = b.make_models(seed, c)
    assert len(models) == 2
print("real_training_table_and_initial_models = PASS; no training or model forwards", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 538; protected_inputs = 950", flush=True)
print("manifest_sha256 =", b.MANIFEST_SHA, flush=True)
print("scope = mixed-length candidate trains on three-character TRAIN examples; NOT unseen-length success", flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C282 parent precheck failed" }
    Write-Output "=== C282 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c282_mixed_length_training -v
    if ($LASTEXITCODE -ne 0) { throw "C282 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c282_mixed_length_training as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C282 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C282 scientific training execution ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c282-v5b-mixed-length-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c282_mixed_length_training --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C282 training execution failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c282_mixed_length_training as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:10]]
head = sys.argv[10]
assert len(sys.argv) == 11 and len(paths) == 8
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context().audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
for name in ("candidate_gate", "seed_pass_counts", "two_char_pass_counts", "triple_pass_counts"):
    print(name, "=", s[name], flush=True)
for m in metrics:
    print("C282 model", m["seed"], m["arm"], "two_char=", m["two_char"]["passed"], "triple=", m["triple"]["passed"], flush=True)
for row in s["contrasts"]:
    print("C282 contrast", json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_mixed_length_scores = PASS; unseen_length_success_claim = False; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C282 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C282 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
