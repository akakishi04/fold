param(
    [Parameter(Mandatory=$true)][string]$C213Summary,
    [Parameter(Mandatory=$true)][string]$C212Summary,
    [Parameter(Mandatory=$true)][string]$C211Summary,
    [Parameter(Mandatory=$true)][string]$C210Summary,
    [Parameter(Mandatory=$true)][string]$C209Summary,
    [Parameter(Mandatory=$true)][string]$C208Summary,
    [Parameter(Mandatory=$true)][string]$C207Summary,
    [Parameter(Mandatory=$true)][string]$C206Summary,
    [Parameter(Mandatory=$true)][string]$C205Summary,
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

Write-Output "=== C214 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05\memory_capsule_bridge.py") (Join-Path $Root "fold_lm\v05_benchmarks\gate_f_c214_memory_capsule_closure.py") (Join-Path $Root "tests_lm\test_v05_c214_memory_capsule_closure.py")
if($LASTEXITCODE -ne 0){throw "C214 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C214 V5-F memory capsule closure ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed condition = map accepted C213 observed memory semantics into fixed-port FOLD-R capsule"
Write-Output "expected_focused_tests = 2115 (2116 loaded -1 exact mutable historical test); Gate_F = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_f_c214_memory_capsule_closure as b
b.precheck(
    Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),
    Path(sys.argv[5]),Path(sys.argv[6]),Path(sys.argv[7]),Path(sys.argv[8]),
    Path(sys.argv[9]),Path(sys.argv[10]),Path(sys.argv[11]),Path(sys.argv[12]),
    Path(sys.argv[13]),Path(sys.argv[14]),Path(sys.argv[15]),Path(sys.argv[16]),
    Path(sys.argv[17]),Path(sys.argv[18]),Path.cwd()
)
print('source_and_artifact_precheck = PASS; accepted C213 memory semantics fixed',flush=True)
'@
& $Python -u -c $Precheck $C213Summary $C212Summary $C211Summary $C210Summary $C209Summary $C208Summary $C207Summary $C206Summary $C205Summary $C204Summary $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary
if($LASTEXITCODE -ne 0){throw "C214 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_f_c214_memory_capsule_closure as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==99
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==2115,f'Expected2115 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c214-v5f-memory-capsule-closure-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C214 regression failed; do not run capsule closure"}
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_f_c214_memory_capsule_closure --c213-summary $C213Summary --c212-summary $C212Summary --c211-summary $C211Summary --c210-summary $C210Summary --c209-summary $C209Summary --c208-summary $C208Summary --c207-summary $C207Summary --c206-summary $C206Summary --c205-summary $C205Summary --c204-summary $C204Summary --c203-summary $C203Summary --c202-summary $C202Summary --c201-summary $C201Summary --c200-summary $C200Summary --c199-summary $C199Summary --c174-summary $C174Summary --c181-summary $C181Summary --c188-summary $C188Summary --output-dir $Out --expected-head $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C214 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import json,sys
from fold_lm.v05_benchmarks import gate_f_c214_memory_capsule_closure as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(
    Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),
    Path(sys.argv[6]),Path(sys.argv[7]),Path(sys.argv[8]),Path(sys.argv[9]),
    Path(sys.argv[10]),Path(sys.argv[11]),Path(sys.argv[12]),Path(sys.argv[13]),
    Path(sys.argv[14]),Path(sys.argv[15]),Path(sys.argv[16]),Path(sys.argv[17]),
    Path(sys.argv[18]),Path(sys.argv[19]),Path.cwd()
)
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[20]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
s=p['validation_summary']
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('supported_snapshots =',s['supported_snapshots'])
print('max_abs_error =',s['max_abs_error'])
print('factor_count_sequence =',s['factor_count_sequence'])
print('assumption_readout_delta =',s['assumption_readout_delta'])
print('end_scope_readout_delta =',s['end_scope_readout_delta'])
print('out_of_scope_status =',s['out_of_scope_status'])
print('numeric_unsafe_status =',s['numeric_unsafe_status'])
print('final_export_factor_ids =',s['final_export_factor_ids'])
print('capsule_closure_gate =',b.gate(s))
'@
    & $Python -u -c $Postcheck $Out $C213Summary $C212Summary $C211Summary $C210Summary $C209Summary $C208Summary $C207Summary $C206Summary $C205Summary $C204Summary $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C214 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C214 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
