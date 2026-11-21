param(
    [Parameter(Mandatory=$true)][string]$C256Summary,
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
$Completed = $false
try {
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c257_unseen_fact_order.py") (Join-Path $Root "tests_lm\test_v05_c257_unseen_fact_order.py")
    if ($LASTEXITCODE -ne 0) { throw "C257 Python syntax preflight failed" }
    Write-Output "python_syntax_preflight = PASS"
    Write-Output "expected_focused_tests = 3337 (3338 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; training = 0; models = 10; model_forwards = 180; rows = 34560"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c257_unseen_fact_order as b
b.precheck(Path(sys.argv[1]),Path.cwd())
parts,refs=b.load_inputs(Path(sys.argv[1]))
novel=b.novel_dataset(parts)
print("source_and_artifact_precheck = PASS; source_pins = 388; protected_inputs = 635",flush=True)
print("unseen_order_dataset_sha256 =",b.digest(novel),flush=True)
print("new_orders =",b.NOVEL,"models =",len(refs),flush=True)
'@
    & $Python -u -c $Precheck $C256Summary
    if ($LASTEXITCODE -ne 0) { throw "C257 parent/order precheck failed" }
    Write-Output "=== C257 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c257_unseen_fact_order -v
    if ($LASTEXITCODE -ne 0) { throw "C257 own tests failed; do not run regression or evaluation" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c257_unseen_fact_order as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C257 focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C257 regression failed; do not run evaluation" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c257-v5b-unseen-order-" + [guid]::NewGuid().ToString("N"))
    Write-Output "=== C257 frozen unseen-order capability evaluation ==="
    & $Python -u -m fold_lm.v05_benchmarks.model_c257_unseen_fact_order --c256-summary $C256Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C257 evaluation failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c257_unseen_fact_order as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,measurements=b.verify_artifacts(out,parent,head)
_,_,_,_,a=b.context()
print("=== C257 DECIDING METRICS; FROZEN UNSEEN FACT ORDERS ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in measurements:
    for split in b.SPLITS:
        for c in r["new_orders"][split]:
            print(f'C257 seed={r["seed"]} arm={r["arm"]} split={split} lang={c["language"]} order={c["permutation"]} '
                f'correct={c["correct"]}/{c["rows"]} query_triplet={c["query_triplet_accuracy"]:.6f} '
                f'evidence_drop={c["evidence_drop"]:.6f} query_drop={c["query_drop"]:.6f} answer_nll={c["answer_nll"]:.6f}')
        for lang,m in r["six_order"][split].items():
            print(f'C257 six_order seed={r["seed"]} arm={r["arm"]} split={split} lang={lang} '
                f'all_six_correct={m["all_six_correct"]}/{m["groups"]}')
print("persisted_unseen_order_logits_and_metrics_replay = PASS; protected_inputs = preserved")
print("C256_verdict_unchanged; new_training = 0; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C256Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C257 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C257 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
