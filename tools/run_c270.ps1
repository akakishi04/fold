param(
    [Parameter(Mandatory=$true)][string]$C269Summary,
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
    Write-Output "=== C270 operational authoring preflight ==="
    Write-Output "preflight_head = $ExpectedHead"

    & $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\model_c270_frozen_triple_identifiers.py") (Join-Path $Root "tests_lm\test_v05_c270_frozen_triple_identifiers.py")
    if ($LASTEXITCODE -ne 0) { throw "C270 Python syntax preflight failed" }

    Write-Output "expected_focused_tests = 3645 (3646 loaded -1 inherited exact exclusion)"
    Write-Output "Gate_F = NOT_PASSED; models = 10; new_training = 0; model_forwards = 810; rows = 77760"

    $Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c270_frozen_triple_identifiers as b
b.precheck(Path(sys.argv[1]),Path.cwd())
_,p267,*_=b.context()
data=p267.dataset();prompts=b.prompt_dataset(data,p267);b.validate_dataset(prompts,data,p267)
print("source_and_artifact_precheck = PASS; source_pins = 466; protected_inputs = 800",flush=True)
print("triple_identifier_dataset_sha256 =",b.DATA_SHA,flush=True)
print("new_training = 0; new_normal_rows_per_model = 864",flush=True)
'@
    & $Python -u -c $Precheck $C269Summary
    if ($LASTEXITCODE -ne 0) { throw "C270 parent/task precheck failed" }

    Write-Output "=== C270 own authoring tests: 24 ==="
    & $Python -u -m unittest tests_lm.test_v05_c270_frozen_triple_identifiers -v
    if ($LASTEXITCODE -ne 0) { throw "C270 own tests failed" }

    $Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import model_c270_frozen_triple_identifiers as b
modules=b.regression_modules(Path.cwd())
assert len(modules)==len(set(modules))==b.manifest()["modules"]
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==b.manifest()["focused_tests"]
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
    Write-Output "=== C270 focused regression preflight ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C270 regression preflight failed" }

    Confirm-Repository
    Write-Output "authoring_runtime_preflight = PASS"
    Write-Output "scientific_execution_started = False"
    return
}

Write-Output "=== C270 scientific execution ==="
Write-Output "execution_head = $ExpectedHead"
Write-Output "authoring_runtime_preflight = PASS (completed before scientific logging)"
Write-Output "expected_focused_tests = 3645"
Write-Output "source_pins = 466; protected_inputs = 800"
Confirm-Repository

$Completed = $false
try {
    $Out = Join-Path $Root ("runs\c270-v5b-triple-identifiers-" + [guid]::NewGuid().ToString("N"))
    & $Python -u -m fold_lm.v05_benchmarks.model_c270_frozen_triple_identifiers --c269-summary $C269Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C270 evaluation failed" }

    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import model_c270_frozen_triple_identifiers as b
out,parent,head=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
b.precheck(parent,Path.cwd())
p,metrics=b.verify_artifacts(out,parent,head)
a=b.context()[-1]
print("=== C270 DECIDING METRICS; FROZEN TRIPLE IDENTIFIERS ===")
print("summary =",out/"summary.json")
print("summary_sha256 =",a.sha(out/"summary.json"))
print("scientific_status =",p["status"])
for k,v in p["validation_summary"].items():print(k,"=",v)
for r in metrics:
    print(f'C270 model seed={r["seed"]} arm={r["arm"]} passed={r["passed"]}')
    for c in r["totals"]:print(f'C270 total seed={r["seed"]} arm={r["arm"]} metrics={c}')
    for c in r["cells"]:print(f'C270 cell seed={r["seed"]} arm={r["arm"]} metrics={c}')
    for c in r["two_order"]:print(f'C270 two_order seed={r["seed"]} arm={r["arm"]} metrics={c}')
print("persisted_triple_identifier_scores = PASS; protected_inputs = preserved")
print("C269_bounded_PASS_unchanged; arbitrary_name_claim = False; Gate_F = NOT_PASSED")
'@
    & $Python -u -c $Postcheck $Out $C269Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C270 artifact postcheck failed" }

    $Completed = $true
}
finally {
    Write-Output "=== C270 POSTCHECK ==="
    Confirm-Repository
    Write-Output "tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
