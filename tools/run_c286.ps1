param(
    [Parameter(Mandatory=$true)][ValidateCount(12,12)][string[]]$Summaries,
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
    Write-Output "=== C286 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c286_cosine_tail_stability.py") (Join-Path $Root "tests_lm\test_v05_c286_cosine_tail_stability.py")
    if ($LASTEXITCODE -ne 0) { throw "C286 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys, torch
from fold_lm.v05_benchmarks import model_c286_cosine_tail_stability as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 12
b.precheck(paths, Path.cwd())
_, previous, transfer, training, c = b.context()
data = c.p267.dataset()
tokens, targets = training.training_tables(data, c)
assert tuple(tokens.shape) == (2, 3, 192, 48)
transfer.validate_dataset(transfer.dataset(data), data, c)
for seed in b.SEEDS:
    _, _, lengths, plan = b.schedule(seed, data["TRAIN"])
    assert int(lengths.sum()) == 400
    assert len(b.make_models(seed, c)) == 2
assert b.learning_rates(b.ARMS[0])[:400] == b.learning_rates(b.ARMS[1])[:400]
assert b.learning_rates(b.ARMS[1])[-1] == .0005
print("real_tables_models_and_lr_schedule = PASS; no training or neural forwards", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 562; protected_inputs = 1001", flush=True)
print("manifest_sha256 =", b.MANIFEST_SHA, flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C286 parent/task precheck failed" }
    Write-Output "=== C286 own authoring tests: 40 ==="
    & $Python -u -m unittest tests_lm.test_v05_c286_cosine_tail_stability -v
    if ($LASTEXITCODE -ne 0) { throw "C286 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c286_cosine_tail_stability as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C286 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C286 late-cosine learning-rate execution ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c286-v5b-cosine-tail-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c286_cosine_tail_stability --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C286 training/evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c286_cosine_tail_stability as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:14]]
head = sys.argv[14]
assert len(sys.argv) == 15 and len(paths) == 12
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[4].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
for name in ("candidate_gate", "quad_pass_counts", "two_char_pass_counts", "triple_pass_counts", "all_tasks_pass_counts", "all_prefixes_matched"):
    print(name, "=", s[name], flush=True)
for row in s["seed_results"]:
    print("C286 model", json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
for row in s["contrasts"]:
    print("C286 contrast", json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_cosine_tail_scores = PASS; primary = four-character; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C286 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C286 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
