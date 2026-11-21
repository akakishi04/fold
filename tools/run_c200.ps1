param(
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

Write-Output "=== C200 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05\structured_task_input_v2.py") (Join-Path $Root "fold_lm\v05_benchmarks\gate_e_c200_acquisition_channel_input.py") (Join-Path $Root "tests_lm\test_v05_c200_acquisition_channel_input.py")
if($LASTEXITCODE -ne 0){throw "C200 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C200 V5-E acquisition-channel input contract ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "v2 layout = exact v1 72-feature prefix + 12 per-fact channel bits"
Write-Output "expected_focused_tests = 1731 (1701 existing +30 new); Gate_E = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c200_acquisition_channel_input as b
b.precheck(Path(sys.argv[1]),Path.cwd())
print('source_and_artifact_precheck = PASS; accepted C199 parent fixed',flush=True)
'@
& $Python -u -c $Precheck $C199Summary
if($LASTEXITCODE -ne 0){throw "C200 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c200_acquisition_channel_input as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==85
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1731,f'Expected1731 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c200-v5e-acquisition-channel-input-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C200 regression failed; do not run diagnostic"}
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c200_acquisition_channel_input --c199-summary $C199Summary --output-dir $Out --expected-head $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C200 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c200_acquisition_channel_input as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(Path(sys.argv[2]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[3]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('mask_roundtrips =',p['summary']['mask_roundtrips'])
print('runtime_cross =',p['summary']['runtime_cross'])
print('hidden_pairs =',p['summary']['hidden_pairs'])
print('malformed_rejected =',p['summary']['malformed_rejected'])
print('v1_prefix_preserved =',p['summary']['v1_prefix_preserved'])
print('candidate_gate_passed =',b.gate(p['summary']))
'@
    & $Python -u -c $Postcheck $Out $C199Summary $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C200 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C200 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
