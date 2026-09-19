param(
    [Parameter(Mandatory=$true)][string]$C196Summary,
    [Parameter(Mandatory=$true)][string]$C195Summary,
    [Parameter(Mandatory=$true)][string]$C194Summary,
    [Parameter(Mandatory=$true)][string]$C193Summary,
    [Parameter(Mandatory=$true)][string]$C192Summary,
    [Parameter(Mandatory=$true)][string]$C191Summary,
    [Parameter(Mandatory=$true)][string]$C190Summary,
    [Parameter(Mandatory=$true)][string]$C189Summary,
    [Parameter(Mandatory=$true)][string]$C188Summary,
    [Parameter(Mandatory=$true)][string]$C187Summary,
    [Parameter(Mandatory=$true)][string]$C186Summary,
    [Parameter(Mandatory=$true)][string]$C185Summary,
    [Parameter(Mandatory=$true)][string]$C184Summary,
    [Parameter(Mandatory=$true)][string]$C183Summary,
    [Parameter(Mandatory=$true)][string]$C182Summary,
    [Parameter(Mandatory=$true)][string]$C181Summary,
    [Parameter(Mandatory=$true)][string]$C180Summary,
    [Parameter(Mandatory=$true)][string]$C179Summary,
    [Parameter(Mandatory=$true)][string]$C178Summary,
    [Parameter(Mandatory=$true)][string]$C177Summary,
    [Parameter(Mandatory=$true)][string]$C176Summary,
    [Parameter(Mandatory=$true)][string]$C174Summary,
    [Parameter(Mandatory=$true)][string]$ExpectedHead
)
$ErrorActionPreference="Stop"
$PSNativeCommandUseErrorActionPreference=$false
Set-StrictMode -Version Latest
$Root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python=Join-Path $Root ".venv-py31315\Scripts\python.exe"
$ParentPaths=@($C196Summary,$C195Summary,$C194Summary,$C193Summary,$C192Summary,$C191Summary,
    $C190Summary,$C189Summary,$C188Summary,$C187Summary,$C186Summary,$C185Summary,$C184Summary,
    $C183Summary,$C182Summary,$C181Summary,$C180Summary,$C179Summary,$C178Summary,$C177Summary,
    $C176Summary,$C174Summary) | ForEach-Object {(Resolve-Path -LiteralPath $_).Path}
$Names=@("c196","c195","c194","c193","c192","c191","c190","c189","c188","c187","c186",
    "c185","c184","c183","c182","c181","c180","c179","c178","c177","c176","c174")

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
Write-Output "=== C197 authoring syntax preflight ==="
& $Python -m py_compile `
    (Join-Path $Root "fold_lm\v05_benchmarks\gate_e_c197_provider_failure_generic_loop.py") `
    (Join-Path $Root "tests_lm\test_v05_c197_provider_failure_generic_loop.py")
if($LASTEXITCODE -ne 0){throw "C197 Python syntax preflight failed"}
Write-Output "python_syntax_preflight = PASS"
Write-Output "=== FOLD C197 V5-E provider-failure reason propagation ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed rule = non-admitted dispatch reason becomes generic-loop unresolved terminal reason"
Write-Output "arms = ALLOWED exact C196/C194 replay + PROVIDER_FAILURE_AFTER_RESERVATION"
Write-Output "expected_focused_tests = 1653 (1629 existing +24 new); Gate_E = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c197_provider_failure_generic_loop as b
b.precheck(Path(sys.argv[1]),*(Path(x) for x in sys.argv[2:23]),Path.cwd())
print('source_and_artifact_precheck = PASS; accepted C196 lineage fixed',flush=True)
'@
& $Python -u -c $Precheck @ParentPaths
if($LASTEXITCODE -ne 0){throw "C197 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c197_provider_failure_generic_loop as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==82
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1653,f'Expected1653 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c197-v5e-provider-failure-reason-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C197 regression failed; do not run benchmark"}
    Confirm-Repository
    $Cli=@("--output-dir",$Out,"--expected-head",$ExpectedHead)
    for($i=0;$i -lt $ParentPaths.Count;$i++){$Cli+=@("--$($Names[$i])-summary",$ParentPaths[$i])}
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c197_provider_failure_generic_loop @Cli
    if($LASTEXITCODE -ne 0){throw "C197 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c197_provider_failure_generic_loop as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(Path(sys.argv[2]),*(Path(x) for x in sys.argv[3:24]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[24]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('allowed_blocks =',len(p['allowed_records']))
print('failure_blocks =',len(p['failure_records']))
print('provider_failures =',sum(r['failure_attempts'] for r in p['failure_records']))
print('provider_calls =',sum(r['provider_calls'] for r in p['failure_records']))
print('failure_publications =',sum(r['publications'] for r in p['failure_records']))
print('failure_retries =',sum(r['retries'] for r in p['failure_records']))
print('candidate_gate_passed =',b.gate(p['allowed_records'],p['failure_records']))
'@
    & $Python -u -c $Postcheck $Out @ParentPaths $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C197 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C197 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
