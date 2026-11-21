param(
    [Parameter(Mandatory=$true)][string]$C243Summary,
    [Parameter(Mandatory=$true)][string]$C242Summary,
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
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c244_two_partner_recombination.py") (Join-Path $Root "tests_lm\test_v05_c244_two_partner_recombination.py")
if ($LASTEXITCODE -ne 0) { throw "C244 Python syntax failed" }
Write-Output "python_syntax_preflight = PASS"
Write-Output "expected_focused_tests = 3025 (3026 loaded -1 inherited exact exclusion)"
Write-Output "Gate_F = NOT_PASSED; TRAIN64; HOLDOUT32; batch32 alternating; training_steps = 2400"
Write-Output "expected_model_forward_calls = 2490; expected_row_presentations = 81408"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as b
parent, old = Path(sys.argv[1]), Path(sys.argv[2])
b.precheck(parent, old, Path.cwd())
parts, refs, comparator = b.load_inputs(old)
print("source_and_artifact_precheck = PASS; source_pins = 310; protected_inputs = 478", flush=True)
print("two_partner_train_audit = PASS; other_value_lookup_ceiling = 0.50; query_only_ceiling = 0.25", flush=True)
print("partition_rows =", {s: len(r) for s, r in parts.items()}, flush=True)
print("C242_comparator = same HOLDOUT32 only; NLL_not_recomputed", flush=True)
'@
& $Python -u -c $Precheck $C243Summary $C242Summary
if ($LASTEXITCODE -ne 0) { throw "C244 parent/data/schedule precheck failed" }
$Regression = @'
from pathlib import Path
import sys, unittest
from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as b
names = b.regression_modules(Path.cwd())
assert len(names) == len(set(names)) == b.manifest()["modules"]
suite = b.regression_suite(Path.cwd())
assert suite.countTestCases() == b.manifest()["focused_tests"]
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c244-v5b-two-partner-recombination-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== C244 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c244_two_partner_recombination -v
    if ($LASTEXITCODE -ne 0) { throw "C244 own tests failed; do not run regression or probe" }
    Write-Output "authoring_selftest = PASS"
    Write-Output "=== C244 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C244 regression failed; do not run probe" }
    Confirm-Repository
    Write-Output "=== C244 fresh two-partner recombination probe ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c244_two_partner_recombination --c243-summary $C243Summary --c242-summary $C242Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C244 execution failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as b
out, parent, old, head = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
b.precheck(parent, old, Path.cwd())
p, rows = b.verify_artifacts(out, old, head)
_, _, _, _, a = b.context()
print("=== C244 DECIDING METRICS; TWO-PARTNER TRAIN64 / COMMON HOLDOUT32 ===")
print("summary =", out / "summary.json")
print("summary_sha256 =", a.sha(out / "summary.json"))
print("scientific_status =", p["status"])
for k, v in p["validation_summary"].items(): print(k, "=", v)
for r in rows:
    print("block_updates =", r["seed"], r["family"], r["block_updates"])
    for split in b.SPLITS:
        for lang, m in r["final"][split].items():
            print(f'C244 seed={r["seed"]} family={r["family"]} split={split} lang={lang} '
                  f'rows={m["rows"]} accuracy={m["accuracy"]:.6f} fact_pair={m["fact_pair_accuracy"]:.6f} '
                  f'query_pair={m["query_pair_accuracy"]:.6f} order_pair={m["order_pair_accuracy"]:.6f} '
                  f'evidence_drop={m["evidence_drop"]:.6f} query_drop={m["query_drop"]:.6f} answer_nll={m["answer_nll"]:.6f}')
    for lang, c in r["c242_same_holdout_discrete"].items():
        now = r["final"]["HOLDOUT"][lang]["accuracy"]
        print(f'C244 common_holdout seed={r["seed"]} family={r["family"]} lang={lang} '
              f'C242_accuracy={c["accuracy"]:.6f} C244_accuracy={now:.6f} delta={now-c["accuracy"]:.6f}')
print("persisted_partition_comparator_and_discrete_replay = PASS; protected_inputs = preserved")
'@
    & $Python -u -c $Postcheck $Out $C243Summary $C242Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C244 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C244 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
