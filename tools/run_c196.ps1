param(
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
$ParentPaths=@($C195Summary,$C194Summary,$C193Summary,$C192Summary,$C191Summary,$C190Summary,
    $C189Summary,$C188Summary,$C187Summary,$C186Summary,$C185Summary,$C184Summary,$C183Summary,
    $C182Summary,$C181Summary,$C180Summary,$C179Summary,$C178Summary,$C177Summary,$C176Summary,
    $C174Summary) | ForEach-Object {(Resolve-Path -LiteralPath $_).Path}
$Names=@("c195","c194","c193","c192","c191","c190","c189","c188","c187","c186","c185",
    "c184","c183","c182","c181","c180","c179","c178","c177","c176","c174")

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
Write-Output "=== FOLD C196 V5-E result-aware generic loop ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "changed rule = continue only after actual OBSERVATION_ADMITTED acquisition"
Write-Output "arms = ALLOWED exact C194 replay + PERMISSION_REVOKED_AFTER_DECISION safe denial"
Write-Output "expected_focused_tests = 1629 (1605 existing +24 new); Gate_E = NOT_PASSED"

$Precheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as b
b.precheck(Path(sys.argv[1]),*(Path(x) for x in sys.argv[2:22]),Path.cwd())
print('source_and_artifact_precheck = PASS; accepted C195 lineage and C194 reference fixed',flush=True)
'@
& $Python -u -c $Precheck @ParentPaths
if($LASTEXITCODE -ne 0){throw "C196 source/artifact precheck failed"}

$Regression=@'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==81
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1629,f'Expected1629 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@

$Out=Join-Path $Root ("runs\c196-v5e-result-aware-loop-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed=$false
try{
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if($LASTEXITCODE -ne 0){throw "C196 regression failed; do not run benchmark"}
    Confirm-Repository
    $Cli=@("--output-dir",$Out,"--expected-head",$ExpectedHead)
    for($i=0;$i -lt $ParentPaths.Count;$i++){$Cli+=@("--$($Names[$i])-summary",$ParentPaths[$i])}
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c196_result_aware_generic_loop @Cli
    if($LASTEXITCODE -ne 0){throw "C196 execution failed; preserve invalid.json"}

    $Postcheck=@'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(Path(sys.argv[2]),*(Path(x) for x in sys.argv[3:23]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[23]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('allowed_blocks =',len(p['allowed_records']))
print('denied_blocks =',len(p['denied_records']))
print('denied_attempts =',sum(r['denied_attempts'] for r in p['denied_records']))
print('denied_provider_calls =',sum(r['provider_calls'] for r in p['denied_records']))
print('denied_retries =',sum(r['retries'] for r in p['denied_records']))
print('candidate_gate_passed =',b.gate(p['allowed_records'],p['denied_records']))
'@
    & $Python -u -c $Postcheck $Out @ParentPaths $ExpectedHead
    if($LASTEXITCODE -ne 0){throw "C196 artifact postcheck failed"}
    $Completed=$true
}
finally{
    Write-Output "=== C196 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
