param(
    [Parameter(Mandatory=$true)][string]$C203Summary,
    [Parameter(Mandatory=$true)][string]$C202Summary,
    [Parameter(Mandatory=$true)][string]$C201Summary,
    [Parameter(Mandatory=$true)][string]$C200Summary,
    [Parameter(Mandatory=$true)][string]$C199Summary,
    [Parameter(Mandatory=$true)][string]$C174Summary,
    [Parameter(Mandatory=$true)][string]$C181Summary,
    [Parameter(Mandatory=$true)][string]$C188Summary,
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

Write-Output "=== C204 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\gate_e_c204_live_v2_mixed_channel_loop.py") (Join-Path $Root "tests_lm\test_v05_c204_live_v2_mixed_channel_loop.py")
if($LASTEXITCODE -ne 0){throw "C204 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C204 V5-E live-v2 mixed-channel loop ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed condition = saved trace replay -> live frozen C181/C188 inference"
Write-Output "expected_focused_tests = 1845 (1813 existing +32 new); Gate_E = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c204_live_v2_mixed_channel_loop as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),Path(sys.argv[6]),Path(sys.argv[7]),Path(sys.argv[8]),Path.cwd())
print('source_and_artifact_precheck = PASS; accepted C203/C199/C181/C188 lineage fixed',flush=True)
'@
& $Python -u -c $Precheck $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary
if($LASTEXITCODE -ne 0){throw "C204 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c204_live_v2_mixed_channel_loop as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==89
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1845,f'Expected1845 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c204-v5e-live-v2-mixed-channel-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C204 regression failed; do not run benchmark"}
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c204_live_v2_mixed_channel_loop --c203-summary $C203Summary --c202-summary $C202Summary --c201-summary $C201Summary --c200-summary $C200Summary --c199-summary $C199Summary --c174-summary $C174Summary --c181-summary $C181Summary --c188-summary $C188Summary --output-dir $Out --expected-head $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C204 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c204_live_v2_mixed_channel_loop as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),Path(sys.argv[6]),Path(sys.argv[7]),Path(sys.argv[8]),Path(sys.argv[9]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[10]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('decisions =',p['summary']['decisions'])
print('acquisitions =',p['summary']['acquisitions'])
print('final_sufficient =',p['summary']['final_sufficient'])
print('v2_packets =',p['summary']['v2_packets'])
print('inference_rows =',p['summary']['inference_rows'])
print('channel_counts =',p['summary']['channel_counts'])
print('channel_switches =',p['summary']['channel_switches'])
print('necessity_prediction_errors =',p['summary']['necessity_prediction_errors'])
print('target_prediction_errors =',p['summary']['target_prediction_errors'])
print('max_necessity_logit_delta =',p['summary']['max_necessity_logit_delta'])
print('max_target_logit_delta =',p['summary']['max_target_logit_delta'])
print('v2_prefix_errors =',p['summary']['v2_prefix_errors'])
print('failures =',p['summary']['failures'])
print('candidate_gate_passed =',b.gate(p['block_records'],p['summary']))
'@
    & $Python -u -c $Postcheck $Out $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C204 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C204 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
