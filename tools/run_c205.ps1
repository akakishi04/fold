param(
    [Parameter(Mandatory=$true)][string]$C204Summary,
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

Write-Output "=== C205 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\gate_e_c205_phase0_batch_composition_attribution.py") (Join-Path $Root "tests_lm\test_v05_c205_phase0_batch_composition_attribution.py")
if($LASTEXITCODE -ne 0){throw "C205 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C205 V5-E phase0 batch-composition attribution ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed condition = phase0 unique1768 vs direct-expanded9536 frozen inference"
Write-Output "expected_focused_tests = 1870 (1846 existing +24 new); Gate_E = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),Path(sys.argv[6]),Path(sys.argv[7]),Path(sys.argv[8]),Path(sys.argv[9]),Path.cwd())
print('source_and_artifact_precheck = PASS; accepted C204-valid-negative/C199/C181/C188 lineage fixed',flush=True)
'@
& $Python -u -c $Precheck $C204Summary $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary
if($LASTEXITCODE -ne 0){throw "C205 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==90
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1870,f'Expected1870 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c205-v5e-phase0-batch-attribution-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C205 regression failed; do not run diagnostic"}
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c205_phase0_batch_composition_attribution --c204-summary $C204Summary --c203-summary $C203Summary --c202-summary $C202Summary --c201-summary $C201Summary --c200-summary $C200Summary --c199-summary $C199Summary --c174-summary $C174Summary --c181-summary $C181Summary --c188-summary $C188Summary --output-dir $Out --expected-head $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C205 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),Path(sys.argv[6]),Path(sys.argv[7]),Path(sys.argv[8]),Path(sys.argv[9]),Path(sys.argv[10]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[11]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
cu=p['canonical_unique'];ed=p['expanded_direct'];mm=p['c204_max_match']
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('canonical_max_necessity_delta =',max(r['necessity_max_abs_logit_difference'] for r in cu))
print('canonical_max_target_delta =',max(r['target_max_abs_logit_difference'] for r in cu))
print('expanded_max_necessity_delta =',max(r['necessity_max_abs_logit_difference'] for r in ed))
print('expanded_max_target_delta =',max(r['target_max_abs_logit_difference'] for r in ed))
print('max_parent_necessity_match_error =',max(r['necessity_parent_max_delta_difference'] for r in mm))
print('max_parent_target_match_error =',max(r['target_parent_max_delta_difference'] for r in mm))
print('workload =',p['workload'])
print('candidate_gate_passed =',b.gate(cu,ed,mm,p['workload']))
'@
    & $Python -u -c $Postcheck $Out $C204Summary $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C205 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C205 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
