param(
    [Parameter(Mandatory=$true)][ValidateCount(9,9)][string[]]$Summaries,
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
    Write-Output "=== C283 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c283_frozen_four_character_transfer.py") (Join-Path $Root "tests_lm\test_v05_c283_frozen_four_character_transfer.py")
    if ($LASTEXITCODE -ne 0) { throw "C283 Python syntax preflight failed" }
    $Precheck = @'
from pathlib import Path
import sys, torch
from fold_lm.v05_benchmarks import model_c283_frozen_four_character_transfer as b
paths = [Path(x) for x in sys.argv[1:]]
assert len(paths) == 9
b.precheck(paths, Path.cwd())
parent, c = b.context()
data = c.p267.dataset()
quad = b.dataset(data)
b.validate_dataset(quad, data, c)
raw = {}
for split in b.SPLITS:
    raw[split] = {}
    for profile in b.PROFILE_MAP:
        raw[split][profile] = {}
        for view in b.VIEWS:
            items = quad[split][profile]
            tokens = torch.stack([c.factory.prefix_tensor(r["views"][view].encode()) for r in items])
            assert tuple(tokens.shape) == (len(items), 48)
            y = torch.zeros((len(items), 256), dtype=torch.float64)
            labels = [r["target"] if view == "normal" else 0 for r in items]
            y[torch.arange(len(items)), torch.tensor(labels)] = 1.
            raw[split][profile][view] = y
scored = b.score_quad(data, raw, c)
assert scored["passed"] is True and len(scored["cells"]) == 72 and len(scored["two_order"]) == 36
assert sum(x["correct"] for x in scored["totals"]) == 864
for seed in b.SEEDS:
    assert len(parent.make_models(seed, c)) == 2
print("real_quad_tokens_and_scorer_adapter = PASS; no training or neural forwards", flush=True)
print("source_and_artifact_precheck = PASS; source_pins = 544; protected_inputs = 964", flush=True)
print("manifest_sha256 =", b.MANIFEST_SHA, flush=True)
print("quad_dataset_sha256 =", b.QUAD_SHA, flush=True)
'@
    & $Python -u -c $Precheck @Summaries
    if ($LASTEXITCODE -ne 0) { throw "C283 parent/dataset precheck failed" }
    Write-Output "=== C283 own authoring tests: 32 ==="
    & $Python -u -m unittest tests_lm.test_v05_c283_frozen_four_character_transfer -v
    if ($LASTEXITCODE -ne 0) { throw "C283 own tests failed" }
    $Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c283_frozen_four_character_transfer as b
modules = b.regression_modules(Path.cwd())
assert len(modules) == len(set(modules)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
print("expected_focused_tests =", suite.countTestCases(), flush=True)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C283 focused regression failed" }
    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}
Write-Output "=== C283 frozen four-character evaluation ==="
Write-Output "execution_head = $ExpectedHead"
$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c283-v5b-frozen-four-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c283_frozen_four_character_transfer --summaries @Summaries --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C283 frozen evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import json, sys
from fold_lm.v05_benchmarks import model_c283_frozen_four_character_transfer as b
out = Path(sys.argv[1])
paths = [Path(x) for x in sys.argv[2:11]]
head = sys.argv[11]
assert len(sys.argv) == 12 and len(paths) == 9
b.precheck(paths, Path.cwd())
p, metrics = b.verify_artifacts(out, paths, head)
print("summary =", out / "summary.json", flush=True)
print("summary_sha256 =", b.context()[1].audit.sha(out / "summary.json"), flush=True)
print("scientific_status =", p["status"], flush=True)
s = p["validation_summary"]
for name in ("candidate_gate", "seed_pass_counts", "all_replays", "all_weights_preserved"):
    print(name, "=", s[name], flush=True)
for m in metrics:
    print("C283 model", m["seed"], m["arm"], "quad_pass=", m["passed"], flush=True)
for row in s["contrasts"]:
    print("C283 contrast", json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
print("persisted_four_character_scores = PASS; C282 verdict preserved; Gate_F = NOT_PASSED", flush=True)
'@
    & $Python -u -c $Postcheck $Out @Summaries $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C283 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C283 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
