param(
    [Parameter(Mandatory=$true)][ValidateCount(15,15)][string[]]$Summaries,
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
    Write-Output "=== C289 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c289_early_pair_withdrawal.py") (Join-Path $Root "tests_lm\test_v05_c289_early_pair_withdrawal.py")
    if ($LASTEXITCODE -ne 0) { throw "C289 syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys, torch
from fold_lm.v05_benchmarks import model_c289_early_pair_withdrawal as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 15
b.precheck(paths, Path.cwd())
parent, _, _, transfer, training, c = b.context()
data = c.p267.dataset()
tokens, targets = training.training_tables(data, c)
assert tuple(tokens.shape) == (2, 3, 192, 48)
assert torch.equal(targets, torch.tensor([r["target"] for r in data["TRAIN"]]))
transfer.validate_dataset(transfer.dataset(data), data, c)
for seed in b.SEEDS:
    ids, _, _, plan = b.schedule(seed, data["TRAIN"])
    assert bool((targets[ids[:, 0::2]] != targets[ids[:, 1::2]]).all())
    assert len(b.make_models(seed, c)) == 3
z = torch.linspace(-1, 1, 512, dtype=torch.float64).reshape(2, 256)
y = torch.tensor([48, 49])
for weight, arm in ((0., "ce_only"), (.25, "ce_pair_assignment")):
    assert all(torch.equal(a, d) for a, d in zip(b.objective(z, y, weight), parent.objective(z, y, arm), strict=True))
assert b.weight_schedule("pair_early") == [.25]*400 + [0.]*400
print("real_tables_three_models_parent_objective_and_switch = PASS; no neural forwards", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 580; protected_inputs = 1041", flush=True)
print("manifest_sha256 =", b.MANIFEST_SHA, flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C289 parent/task precheck failed" }
    Write-Output "=== C289 own authoring tests: 48 ==="
    & $Python -u -m unittest tests_lm.test_v05_c289_early_pair_withdrawal -v
    if ($LASTEXITCODE -ne 0) { throw "C289 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c289_early_pair_withdrawal as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C289 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C289 early pair-loss withdrawal training ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c289-v5b-early-pair-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c289_early_pair_withdrawal --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C289 training/evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c289_early_pair_withdrawal as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:17]]
head = sys.argv[17]
assert len(sys.argv) == 18 and len(paths) == 15
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[5].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
for name in ("candidate_gate", "quad_pass_counts", "two_char_pass_counts", "triple_pass_counts", "all_tasks_pass_counts", "fitted_train_pass_counts", "seen_holdout_pass_counts", "all_auxiliary_prefixes_matched"):
    print(name, "=", s[name], flush=True)
for name in ("seed_results", "contrasts", "final_partitions"):
    for row in s[name]:
        print("C289", name, json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_early_pair_scores = PASS; primary = four-character; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C289 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C289 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
