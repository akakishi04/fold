param(
    [Parameter(Mandatory = $true)][string]$C174Summary,
    [Parameter(Mandatory = $true)][string]$ExpectedHead
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python = Join-Path $Root ".venv-py31315\Scripts\python.exe"
$C174Summary = (Resolve-Path -LiteralPath $C174Summary).Path
$Protected = @(
    @{Path = (Join-Path $Root "runs\chatgpt-last-result.json"); Hash = "fd4a8da897bdaea9d103a252e30212c7ff842d23300d7c837333e146dee51931"},
    @{Path = (Join-Path $Root "runs\fixtures\v05-c-composition-20260921.pt"); Hash = "a52f8209703149407580f7e2965b61b78653030ee992af6d759865736741ca9e"},
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
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Authoritative Python is missing" }
Confirm-Repository
Write-Output "=== FOLD C175 V5-E frozen prediction frequency reference ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "stored model predictions = 311040; TRAIN-only blind keys = 81; new reference predictions = 51840"
Write-Output "benchmark training = 0; model forwards = 0; checkpoint deserializations = 0; new seeds = 0"
Write-Output "same four pilot groups; post-C174 development analysis, not independent confirmation"
Write-Output "expected_focused_tests = 973 (953 existing + 20 new); Gate_E = NOT_PASSED"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as b
parent=b.load_parent(sys.argv[1])
b.protect_sources(Path.cwd(),parent);b.protect_artifacts(sys.argv[1],parent)
print('source_and_artifact_precheck = PASS',flush=True)
'@
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c174_learned_necessity as old
names=old.regression_modules(Path.cwd())+['tests_lm.test_v05_c175_frozen_prediction_audit']
assert len(names)==len(set(names))==59
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==973, f'Expected973 tests, got{suite.countTestCases()}'
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'@
$Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as b
out=Path(sys.argv[1]);parent=b.load_parent(sys.argv[2]);b.protect_sources(Path.cwd(),parent)
b.protect_artifacts(sys.argv[2],parent);p=b.read_json(out/'summary.json')
assert p['experiment_id']==b.EXPERIMENT_ID and p['commit_sha']==sys.argv[3]
assert p['diagnostic_execution_valid'] is True
assert p['replayed_model_predictions']==311040 and p['reference_predictions']==51840 and p['blind_keys']==81
assert all(p[k]==0 for k in ('new_training_steps','new_model_forwards','fresh_seeds','checkpoint_deserializations','actual_acquisitions','evidence_writes','network_calls'))
assert p['status']==('PASS' if b.gate(p['pairs'],p['reference']) else 'FAIL')
for name,want in p['input_sha256'].items(): assert b.sha(name)==want,name
for item in p['artifacts']:
    path=b.safe_child(out,item['file'])
    assert b.sha(path)==item['sha256'] and path.stat().st_size==item['serialized_bytes'],str(path)
print('summary =',out/'summary.json')
print('summary_sha256 =',b.sha(out/'summary.json'))
print('scientific_status =',p['status'])
'@
$Out = Join-Path $Root ("runs\c175-v5e-frozen-predictions-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    & $Python -u -c $Precheck $C174Summary
    if ($LASTEXITCODE -ne 0) { throw "C175 source/artifact precheck failed" }
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C175 regression failed; do not start audit" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c175_frozen_prediction_audit `
        --c174-summary $C174Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C175 execution failed; preserve invalid report" }
    & $Python -u -c $Postcheck $Out $C174Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C175 postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C175 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
