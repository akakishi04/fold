param(
    [Parameter(Mandatory=$true)][string]$C200Summary,
    [Parameter(Mandatory=$true)][string]$C199Summary,
    [Parameter(Mandatory=$true)][string]$ExpectedHead
)
$ErrorActionPreference="Stop"
$PSNativeCommandUseErrorActionPreference=$false
Set-StrictMode -Version Latest
$Root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python=Join-Path $Root ".venv-py31315\Scripts\python.exe"

function Confirm-Repository {
    $branch=git branch --show-current
    if($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss"){throw "Unexpected branch: $branch"}
    $head=git rev-parse HEAD
    if($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead){throw "Unexpected HEAD: $head"}
    $dirty=@(git status --porcelain --untracked-files=no)
    if($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0){throw "Tracked tree must be clean"}
}
if(-not(Test-Path -LiteralPath $Python -PathType Leaf)){throw "Authoritative Python missing"}
Confirm-Repository

Write-Output "=== C201 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05\structured_action_channel.py") (Join-Path $Root "fold_lm\v05_benchmarks\gate_e_c201_selected_fact_channel_route.py") (Join-Path $Root "tests_lm\test_v05_c201_selected_fact_channel_route.py")
if($LASTEXITCODE -ne 0){throw "C201 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C201 V5-E selected-fact channel routing ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "target source = accepted C199 ALLOWED phase0 saved target"
Write-Output "expected_focused_tests = 1759 (1731 existing +28 new); Gate_E = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
print('source_and_artifact_precheck = PASS; accepted C200/C199 parents fixed',flush=True)
'@
& $Python -u -c $Precheck $C200Summary $C199Summary
if($LASTEXITCODE -ne 0){throw "C201 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==86
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1759,f'Expected1759 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c201-v5e-selected-fact-channel-route-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C201 regression failed; do not run diagnostic"}
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c201_selected_fact_channel_route --c200-summary $C200Summary --c199-summary $C199Summary --output-dir $Out --expected-head $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C201 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(Path(sys.argv[2]),Path(sys.argv[3]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[4]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('route_cases =',p['summary']['route_cases'])
print('route_mismatches =',p['summary']['route_mismatches'])
print('authority_cross =',p['summary']['authority_cross'])
print('authority_failures =',p['summary']['authority_failures'])
print('observed_controls =',p['summary']['observed_controls'])
print('invalid_mapper_rejected =',p['summary']['invalid_mapper_rejected'])
print('candidate_gate_passed =',b.gate(p['summary']))
'@
    & $Python -u -c $Postcheck $Out $C200Summary $C199Summary $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C201 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C201 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
