param(
    [Parameter(Mandatory=$true)][ValidateCount(14,14)][string[]]$Summaries,
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
    Write-Output "=== C288 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c288_query_pair_assignment_loss.py") (Join-Path $Root "tests_lm\test_v05_c288_query_pair_assignment_loss.py")
    if ($LASTEXITCODE -ne 0) { throw "C288 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys, torch
from fold_lm.v05_benchmarks import model_c288_query_pair_assignment_loss as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 14
b.precheck(paths, Path.cwd())
_, _, transfer, training, c = b.context()
data = c.p267.dataset()
tokens, targets = training.training_tables(data, c)
assert tuple(tokens.shape) == (2, 3, 192, 48)
assert torch.equal(targets, torch.tensor([r["target"] for r in data["TRAIN"]]))
transfer.validate_dataset(transfer.dataset(data), data, c)
for seed in b.SEEDS:
    ids, _, _, plan = b.schedule(seed, data["TRAIN"])
    assert bool((targets[ids[:, 0::2]] != targets[ids[:, 1::2]]).all())
    assert len(b.make_models(seed, c)) == 2
print("real_tables_pairs_and_initial_models = PASS; no training or neural forwards", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 574; protected_inputs = 1026", flush=True)
print("manifest_sha256 =", b.MANIFEST_SHA, flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C288 parent/task precheck failed" }
    Write-Output "=== C288 own authoring tests: 40 ==="
    & $Python -u -m unittest tests_lm.test_v05_c288_query_pair_assignment_loss -v
    if ($LASTEXITCODE -ne 0) { throw "C288 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c288_query_pair_assignment_loss as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C288 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C288 query-pair assignment training ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c288-v5b-pair-assignment-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c288_query_pair_assignment_loss --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C288 training/evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c288_query_pair_assignment_loss as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:16]]
head = sys.argv[16]
assert len(sys.argv) == 17 and len(paths) == 14
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[4].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
for name in ("candidate_gate", "quad_pass_counts", "two_char_pass_counts", "triple_pass_counts", "all_tasks_pass_counts", "fitted_train_pass_counts", "seen_holdout_pass_counts"):
    print(name, "=", s[name], flush=True)
for name in ("seed_results", "contrasts", "final_partitions"):
    for row in s[name]:
        print("C288", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_pair_assignment_scores = PASS; primary = four-character; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C288 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C288 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
