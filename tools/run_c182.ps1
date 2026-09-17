param(
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
$C181Summary = (Resolve-Path -LiteralPath $C181Summary).Path
$C180Summary = (Resolve-Path -LiteralPath $C180Summary).Path
$C179Summary = (Resolve-Path -LiteralPath $C179Summary).Path
$C178Summary = (Resolve-Path -LiteralPath $C178Summary).Path
$C177Summary = (Resolve-Path -LiteralPath $C177Summary).Path
$C176Summary = (Resolve-Path -LiteralPath $C176Summary).Path
$C174Summary = (Resolve-Path -LiteralPath $C174Summary).Path
$Protected = @(
    @{Path = (Join-Path $Root "runs\chatgpt-last-result.json"); Hash = "fd4a8da897bdaea9d103a252e30212c7ff842d23300d7c837333e146dee51931"},
    @{Path = (Join-Path $Root "runs\fixtures\v05-c-composition-20260921.pt"); Hash = "a52f8209703149407580f7e2965b61b78653030ee992af6d759865736741ca9e"},
    @{Path = $C181Summary; Hash = "bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98"},
    @{Path = $C180Summary; Hash = "9ad6eb52054388abda89d2eb8254b2ce278bfc983ae2a6375ab7d8327f91adf2"},
    @{Path = $C179Summary; Hash = "ba7488e2002894ccf614c29e84e0d50594dfba7617abfd8d9f4b64442915767b"},
    @{Path = $C178Summary; Hash = "19bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8"},
    @{Path = $C177Summary; Hash = "99f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4"},
    @{Path = $C176Summary; Hash = "b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b"},
    @{Path = $C174Summary; Hash = "3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36"}
)
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
Write-Output "=== FOLD C182 V5-E frozen fact-index renaming ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "source seeds = 181001/181002/181003; six frozen C181 checkpoints; fresh seeds = 0"
Write-Output "original base only; no teacher/head construction, training or prediction repair"
Write-Output "311040 identity replay rows + 1296648 renamed predictions; all 23 nonidentity permutations"
Write-Output "new numeric inputs, SAME development semantic problems; not independent holdout or Gate E"
Write-Output "CPU float32 threads2; expected_focused_tests = 1185 (1153 existing + 32 new)"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as b
b.precheck(*(Path(x) for x in sys.argv[1:8]),Path.cwd())
print('source_and_artifact_precheck = PASS',flush=True)
'@
& $Python -u -c $Precheck $C181Summary $C180Summary $C179Summary $C178Summary $C177Summary $C176Summary $C174Summary
if ($LASTEXITCODE -ne 0) { throw "C182 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==66
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1185,f'Expected1185 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c182-v5e-frozen-renaming-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C182 regression failed; do not run benchmark" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c182_frozen_fact_renaming `
        --c181-summary $C181Summary --c180-summary $C180Summary --c179-summary $C179Summary `
        --c178-summary $C178Summary --c177-summary $C177Summary --c176-summary $C176Summary `
        --c174-summary $C174Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C182 execution failed; preserve invalid.json" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1]);b.precheck(*(Path(x) for x in sys.argv[2:9]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[9]
assert sum(r['rows'] for r in p['replay'])==311040
assert all(r['decisions_equal'] and r['max_abs_logit_difference']<=b.REPLAY_ATOL for r in p['replay'])
assert sum(r['n'] for r in p['records'])==1296648
for name,want in p['input_sha256'].items():assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
'@
    & $Python -u -c $Postcheck $Out $C181Summary $C180Summary $C179Summary $C178Summary $C177Summary $C176Summary $C174Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C182 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C182 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
