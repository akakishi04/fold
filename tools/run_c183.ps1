param(
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
$Sources = @($C182Summary, $C181Summary, $C180Summary, $C179Summary, $C178Summary, $C177Summary, $C176Summary, $C174Summary)
$Sources = @($Sources | ForEach-Object { (Resolve-Path -LiteralPath $_).Path })
$Protected = @(
    @{Path = (Join-Path $Root "runs\chatgpt-last-result.json"); Hash = "fd4a8da897bdaea9d103a252e30212c7ff842d23300d7c837333e146dee51931"},
    @{Path = (Join-Path $Root "runs\fixtures\v05-c-composition-20260921.pt"); Hash = "a52f8209703149407580f7e2965b61b78653030ee992af6d759865736741ca9e"},
    @{Path = $Sources[0]; Hash = "06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73"}
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
Write-Output "=== FOLD C183 V5-E frozen renaming path attribution ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "six frozen C181 checkpoints; source seeds181001/2/3; no fresh seed or training"
Write-Output "identity and failed permutation17; all9396rows; original base inference and two isolated readouts"
Write-Output "hybrid activations are diagnostic, not legal complete task inputs or a replacement policy"
Write-Output "expected_focused_tests = 1217 (1185 existing + 32 new); Gate_E = NOT_PASSED"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c183_frozen_path_attribution as b
b.precheck(*(Path(x) for x in sys.argv[1:9]),Path.cwd())
print('source_and_artifact_precheck = PASS',flush=True)
'@
& $Python -u -c $Precheck @Sources
if ($LASTEXITCODE -ne 0) { throw "C183 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c183_frozen_path_attribution as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==67
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1217,f'Expected1217 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c183-v5e-path-attribution-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C183 regression failed; do not run benchmark" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c183_frozen_path_attribution `
        --c182-summary $Sources[0] --c181-summary $Sources[1] --c180-summary $Sources[2] `
        --c179-summary $Sources[3] --c178-summary $Sources[4] --c177-summary $Sources[5] `
        --c176-summary $Sources[6] --c174-summary $Sources[7] `
        --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C183 execution failed; preserve invalid.json" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c183_frozen_path_attribution as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1]);b.precheck(*(Path(x) for x in sys.argv[2:10]),Path.cwd())
p=audit.read_json(out/'summary.json');b.validate_result(p)
assert p['commit_sha']==sys.argv[10]
assert sum(r['rows'] for r in p['replay'])==112752
assert all(r['decisions_equal'] and r['max_abs_logit_difference']<=b.REPLAY_ATOL for r in p['replay'])
for name,want in p['input_sha256'].items():assert audit.sha(name)==want,name
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
print('counterexample_path_mode =',p['failure_cases'][0]['mode'])
'@
    & $Python -u -c $Postcheck $Out @Sources $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C183 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C183 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
