param(
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

Write-Output "=== C210 authoring syntax preflight ==="
& $Python -m py_compile (Join-Path $Root "fold_lm\v05_benchmarks\gate_e_c210_baseline_development_measurement.py") (Join-Path $Root "tests_lm\test_v05_c210_baseline_development_measurement.py")
if($LASTEXITCODE -ne 0){throw "C210 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"

Write-Output "=== FOLD C210 V5-E baseline development measurement ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed condition = matched development measurement only; no performance threshold or candidate selection"
Write-Output "expected_focused_tests = 1997 (1998 loaded -1 exact mutable historical test); Gate_E = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c210_baseline_development_measurement as b
b.precheck(
    Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),
    Path(sys.argv[6]),Path(sys.argv[7]),Path(sys.argv[8]),Path(sys.argv[9]),Path(sys.argv[10]),
    Path(sys.argv[11]),Path(sys.argv[12]),Path(sys.argv[13]),Path(sys.argv[14]),Path.cwd()
)
print('source_and_artifact_precheck = PASS; accepted C209/C207 development identities fixed',flush=True)
'@
& $Python -u -c $Precheck $C209Summary $C208Summary $C207Summary $C206Summary $C205Summary $C204Summary $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary
if($LASTEXITCODE -ne 0){throw "C210 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c210_baseline_development_measurement as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==95
suite=b.regression_suite(Path.cwd())
assert suite.countTestCases()==1997,f'Expected1997 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c210-v5e-baseline-development-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C210 regression failed; do not run measurement"}
    Confirm-Repository

    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c210_baseline_development_measurement --c209-summary $C209Summary --c208-summary $C208Summary --c207-summary $C207Summary --c206-summary $C206Summary --c205-summary $C205Summary --c204-summary $C204Summary --c203-summary $C203Summary --c202-summary $C202Summary --c201-summary $C201Summary --c200-summary $C200Summary --c199-summary $C199Summary --c174-summary $C174Summary --c181-summary $C181Summary --c188-summary $C188Summary --output-dir $Out --expected-head $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C210 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import json,sys
from fold_lm.v05_benchmarks import gate_e_c210_baseline_development_measurement as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(
    Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),Path(sys.argv[6]),
    Path(sys.argv[7]),Path(sys.argv[8]),Path(sys.argv[9]),Path(sys.argv[10]),Path(sys.argv[11]),
    Path(sys.argv[12]),Path(sys.argv[13]),Path(sys.argv[14]),Path(sys.argv[15]),Path.cwd()
)
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[16]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('policy_episode_evaluations =',p['policy_episode_evaluations'])
print('internal_only =',json.dumps(p['policy_summary'][b.POLICY_INTERNAL],sort_keys=True))
print('fixed_acquisition =',json.dumps(p['policy_summary'][b.POLICY_FIXED],sort_keys=True))
for pid in b.POLICY_IDS[2:]:
    s=p['policy_summary'][pid]
    print(pid,'=',json.dumps({
        'correct':s['correct'],'answered':s['answered'],'wrong_abstention':s['wrong_abstention'],
        'attempts':s['acquisition_attempts'],'provider_calls':s['provider_calls'],
        'publications':s['publications'],'user_turns':s['user_turns'],
        'unnecessary_acquisition':s['unnecessary_acquisition'],
        'missed_necessary_acquisition':s['missed_necessary_acquisition'],
        'premature_sufficient':s['premature_sufficient'],
        'repeated_need_after_success':s['repeated_need_after_success'],
        'invalid_target':s['invalid_target'],
        'inference_rows':s['inference_rows']
    },sort_keys=True))
print('measurement_complete =',b.measurement_complete(
    p['policy_summary'],p['candidate_model_summary'],p['episode_results']))
print('numerical_margin_registration =',p['numerical_margin_registration'])
print('candidate_selection =',p['candidate_selection'])
print('independent_holdout_created =',p['independent_holdout_created'])
'@
    & $Python -u -c $Postcheck $Out $C209Summary $C208Summary $C207Summary $C206Summary $C205Summary $C204Summary $C203Summary $C202Summary $C201Summary $C200Summary $C199Summary $C174Summary $C181Summary $C188Summary $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C210 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C210 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
