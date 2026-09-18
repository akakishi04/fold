param(
    [Parameter(Mandatory = $true)][string]$C187Summary,
    [Parameter(Mandatory = $true)][string]$C186Summary,
    [Parameter(Mandatory = $true)][string]$C185Summary,
    [Parameter(Mandatory = $true)][string]$C184Summary,
    [Parameter(Mandatory = $true)][string]$C183Summary,
    [Parameter(Mandatory = $true)][string]$C182Summary,
    [Parameter(Mandatory = $true)][string]$C181Summary,
    [Parameter(Mandatory = $true)][string]$C180Summary,
    [Parameter(Mandatory = $true)][string]$C179Summary,
    [Parameter(Mandatory = $true)][string]$C178Summary,
    [Parameter(Mandatory = $true)][string]$C177Summary,
    [Parameter(Mandatory = $true)][string]$C176Summary,
    [Parameter(Mandatory = $true)][string]$C174Summary,
    [Parameter(Mandatory = $true)][string]$ExpectedHead
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python = Join-Path $Root ".venv-py31315\Scripts\python.exe"
$ParentPaths = @($C187Summary, $C186Summary, $C185Summary, $C184Summary, $C183Summary, $C182Summary,
    $C181Summary, $C180Summary, $C179Summary, $C178Summary, $C177Summary, $C176Summary, $C174Summary) |
    ForEach-Object { (Resolve-Path -LiteralPath $_).Path }
$Names = @("c187", "c186", "c185", "c184", "c183", "c182", "c181", "c180", "c179",
    "c178", "c177", "c176", "c174")
$Hashes = @(
    "910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd",
    "e9bfc53b000bb46bc76a00e4e8b78ec5ecc2aa38727610a8a73bf5c5735c1e82",
    "843fb9816270e4a597ca094c6e90408a35910490324db60bc3018f62156ac949",
    "7817f8f17932f772d80e6a994bf58c17c8f71b73a1f5691a4a5345ce3a917e04",
    "ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24",
    "06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73",
    "bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98",
    "9ad6eb52054388abda89d2eb8254b2ce278bfc983ae2a6375ab7d8327f91adf2",
    "ba7488e2002894ccf614c29e84e0d50594dfba7617abfd8d9f4b64442915767b",
    "19bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8",
    "99f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4",
    "b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b",
    "3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36"
)
$Protected = @(
    @{Path = (Join-Path $Root "runs\chatgpt-last-result.json"); Hash = "fd4a8da897bdaea9d103a252e30212c7ff842d23300d7c837333e146dee51931"},
    @{Path = (Join-Path $Root "runs\fixtures\v05-c-composition-20260921.pt"); Hash = "a52f8209703149407580f7e2965b61b78653030ee992af6d759865736741ca9e"}
)
for ($i = 0; $i -lt $ParentPaths.Count; $i++) { $Protected += @{Path = $ParentPaths[$i]; Hash = $Hashes[$i]} }
function Confirm-Repository {
    $Branch = & git branch --show-current
    if ($LASTEXITCODE -ne 0 -or $Branch -ne "feat/sft-target-loss") { throw "Unexpected branch: $Branch" }
    $Head = & git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $Head -ne $ExpectedHead) { throw "Unexpected HEAD: $Head" }
    $Dirty = @(& git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0 -or $Dirty.Count -ne 0) { throw "Tracked tree must be clean" }
    foreach ($Item in $Protected) {
        if ((Get-FileHash -LiteralPath $Item.Path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Item.Hash) {
            throw "Protected hash mismatch: $($Item.Path)"
        }
    }
}
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Authoritative Python missing" }
Confirm-Repository
Write-Output "=== FOLD C188 V5-E multi-missing target selection ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "three frozen accepted C181 INTERNAL_SEMANTICS bases; fresh target-head seeds188001/2/3"
Write-Output "TRAIN discriminating multi-missing rows3824; PILOT primary528; full multi-missing secondary1768"
Write-Output "shared selector455->64ReLU->1; 9 heads; 2000 updates/head; no base update or acquisition"
Write-Output "TRAIN-only syntax-blind frequency reference: m2=268/376 m3=128/152"
Write-Output "expected_focused_tests = 1413 (1377 existing + 36 new); Gate_E = NOT_PASSED"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as b
b.precheck(Path(sys.argv[1]),*(Path(x) for x in sys.argv[2:14]),Path.cwd())
print('source_and_artifact_precheck = PASS; C187 accepted result and lineage fixed',flush=True)
'@
& $Python -u -c $Precheck @ParentPaths
if ($LASTEXITCODE -ne 0) { throw "C188 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==73
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1413,f'Expected1413 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c188-v5e-multimissing-target-selection-" + [guid]::NewGuid().ToString("N"))
Write-Output "output_dir = $Out"
$Completed = $false
try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C188 regression failed; do not run benchmark" }
    Confirm-Repository
    $Cli = @("--output-dir", $Out, "--expected-head", $ExpectedHead)
    for ($i = 0; $i -lt $ParentPaths.Count; $i++) { $Cli += @("--$($Names[$i])-summary", $ParentPaths[$i]) }
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c188_multimissing_target_selection @Cli
    if ($LASTEXITCODE -ne 0) { throw "C188 execution failed; preserve invalid.json" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1])
b.precheck(Path(sys.argv[2]),*(Path(x) for x in sys.argv[3:15]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[15]
for name,want in p['input_sha256'].items(): assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('selector_results =',len(p['selector_results']))
print('frequency_reference_macro =',p['frequency_reference']['macro_m2_m3'])
print('candidate_gate_passed =',b.selector_gate(p['selector_results'],p['frequency_reference']))
'@
    & $Python -u -c $Postcheck $Out @ParentPaths $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C188 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C188 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
