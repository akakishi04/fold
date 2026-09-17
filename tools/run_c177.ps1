param(
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
$C176Summary = (Resolve-Path -LiteralPath $C176Summary).Path
$C174Summary = (Resolve-Path -LiteralPath $C174Summary).Path
$Protected = @(
    @{Path = (Join-Path $Root "runs\chatgpt-last-result.json"); Hash = "fd4a8da897bdaea9d103a252e30212c7ff842d23300d7c837333e146dee51931"},
    @{Path = (Join-Path $Root "runs\fixtures\v05-c-composition-20260921.pt"); Hash = "a52f8209703149407580f7e2965b61b78653030ee992af6d759865736741ca9e"},
    @{Path = $C176Summary; Hash = "b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b"},
    @{Path = $C174Summary; Hash = "3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36"}
)
function Confirm-Repository {
    $Remote = & git remote get-url origin
    if ($LASTEXITCODE -ne 0 -or $Remote -notmatch '[:/]akakishi04/fold(?:\.git)?$') { throw "Unexpected origin: $Remote" }
    $Branch = & git branch --show-current
    if ($LASTEXITCODE -ne 0 -or $Branch -ne "feat/sft-target-loss") { throw "Unexpected branch: $Branch" }
    $Head = & git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $Head -ne $ExpectedHead) { throw "Unexpected HEAD: $Head" }
    $Dirty = @(& git status --porcelain --untracked-files=no)
    if ($LASTEXITCODE -ne 0 -or $Dirty.Count -ne 0) { throw "Tracked tree must be clean" }
    foreach ($Item in $Protected) {
        $Actual = (Get-FileHash -LiteralPath $Item.Path -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($Actual -ne $Item.Hash) { throw "Protected hash mismatch: $($Item.Path)" }
    }
}
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Authoritative Python is missing" }
Confirm-Repository
Write-Output "=== FOLD C177 V5-E frozen score-order audit ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "311040 stored decisions; 56376 pilot scores; 155520 aligned prediction pairs"
Write-Output "no training, model forward, checkpoint loading, threshold search or prediction repair"
Write-Output "C176 remains ACCEPTED VALID NEGATIVE; reused pilot, NOT independent confirmation"
Write-Output "expected_focused_tests = 1025 (1001 existing + 24 new); Gate_E = NOT_PASSED"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
print('source_and_artifact_precheck = PASS',flush=True)
'@
& $Python -u -c $Precheck $C176Summary $C174Summary
if ($LASTEXITCODE -ne 0) { throw "C177 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==61
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1025,f'Expected1025 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c177-v5e-score-order-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C177 regression failed; do not start audit" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c177_frozen_score_order `
        --c176-summary $C176Summary --c174-summary $C174Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C177 execution failed; preserve invalid.json" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1]);b.precheck(Path(sys.argv[2]),Path(sys.argv[3]),Path.cwd())
p=audit.read_json(out/'summary.json')
assert p['experiment_id']==b.EXPERIMENT_ID and p['commit_sha']==sys.argv[4]
assert p['diagnostic_execution_valid'] is True and p['status'] in ('PASS','FAIL')
assert p['replayed_model_predictions']==311040 and p['pilot_score_rows']==56376
assert p['aligned_prediction_pairs']==155520
assert len(p['source_blobs'])==56 and len(p['input_sha256'])==83
for name,want in p['input_sha256'].items():assert audit.sha(name)==want,name
assert len(p['artifacts'])==2 and {a['file'] for a in p['artifacts']}=={'score-order-plan.json','score-order-details.json'}
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
assert ('PASS' if b.gate(p['pairs']) else 'FAIL')==p['status']
for k in ('new_training_steps','model_forwards','checkpoint_deserializations','fresh_seeds','threshold_searches','inference_corrections','actual_acquisitions','evidence_writes','network_calls'):
    assert p[k]==0,k
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
'@
    & $Python -u -c $Postcheck $Out $C176Summary $C174Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C177 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C177 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
