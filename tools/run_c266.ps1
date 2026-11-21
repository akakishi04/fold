param(
    [Parameter(Mandatory=$true)][string]$C265Summary,
    [Parameter(Mandatory=$true)][string]$C264Summary,
    [Parameter(Mandatory=$true)][string]$C263Summary,
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
    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c266_query_pair_audit.py") (Join-Path $Root "tests_lm\test_v05_c266_query_pair_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "C266 Python syntax preflight failed" }
    Write-Output "expected_focused_tests = 3549 (3550 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; diagnostic_only = True; model_forwards = 0; training = 0"
    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c266_query_pair_audit as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path.cwd())
print("source_and_artifact_precheck = PASS; source_pins = 442; protected_inputs = 748",flush=True)
print("saved_normal_answers = 17280; query_pairs = 8640; capability_promotion = False",flush=True)
'@
    & $Python -u -c $Precheck $C265Summary $C264Summary $C263Summary
    if ($LASTEXITCODE -ne 0) { throw "C266 parent precheck failed" }
    Write-Output "=== C266 own authoring tests first: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c266_query_pair_audit -v
    if ($LASTEXITCODE -ne 0) { throw "C266 own tests failed; do not run regression or diagnostic" }
    Write-Output "authoring_selftest = PASS"
    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c266_query_pair_audit as b
modules=b.regression_modules(Path.cwd())
assert len(modules)==len(set(modules))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C266 regression failed; do not run diagnostic" }
    Confirm-Repository
    $Out = Join-Path $Root ("runs\c266-v5b-query-pairs-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c266_query_pair_audit --c265-summary $C265Summary --c264-summary $C264Summary --c263-summary $C263Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C266 saved-answer diagnostic failed" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c266_query_pair_audit as b
out,p265,p264,p263,head=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),sys.argv[5]
b.precheck(p265,p264,p263,Path.cwd())
p,profiles,contrasts=b.verify_artifacts(out,p265,p264,p263,head)
a=b.context()[-1]
print("=== C266 DECIDING METRICS; DIAGNOSTIC ONLY ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in profiles:print("C266 profile =",r)
for r in contrasts:print("C266 matched_contrast =",r)
print("persisted_query_pair_reattribution = PASS; protected_inputs = preserved")
print("C265_valid_negative_unchanged; capability_pass_claim = False; causal_parser_claim = False")
'@
    & $Python -u -c $Postcheck $Out $C265Summary $C264Summary $C263Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C266 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C266 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
