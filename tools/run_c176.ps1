param(
    [Parameter(Mandatory = $true)][string]$C175Summary,
    [Parameter(Mandatory = $true)][string]$C174Summary,
    [Parameter(Mandatory = $true)][string]$ExpectedHead
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python = Join-Path $Root ".venv-py31315\Scripts\python.exe"
$C175Summary = (Resolve-Path -LiteralPath $C175Summary).Path
$C174Summary = (Resolve-Path -LiteralPath $C174Summary).Path
$Protected = @(
    @{Path = (Join-Path $Root "runs\chatgpt-last-result.json"); Hash = "fd4a8da897bdaea9d103a252e30212c7ff842d23300d7c837333e146dee51931"},
    @{Path = (Join-Path $Root "runs\fixtures\v05-c-composition-20260921.pt"); Hash = "a52f8209703149407580f7e2965b61b78653030ee992af6d759865736741ca9e"},
    @{Path = $C175Summary; Hash = "d4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722"},
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
        $Actual = (Get-FileHash -LiteralPath $Item.Path -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($Actual -ne $Item.Hash) { throw "Protected hash mismatch: $($Item.Path)" }
    }
}
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Authoritative Python is missing" }
Confirm-Repository
Write-Output "=== FOLD C176 V5-E missing-count conditional loss ==="
Write-Output "repository = akakishi04/fold; branch = feat/sft-target-loss; commit = $ExpectedHead"
Write-Output "seeds = 176001/176002/176003; 6 new models; unchanged MLP26114; CPU float32 threads2"
Write-Output "steps = 2000/model; batch256; same row schedule; ONLY TRAIN loss weights change"
Write-Output "same reused four pilot groups; NOT independent holdout confirmation"
Write-Output "expected_focused_tests = 1001 (973 existing + 28 new); Gate_E = NOT_PASSED"
$Precheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c176_conditional_loss as b
b.precheck(Path(sys.argv[1]),Path(sys.argv[2]),Path.cwd())
print('source_and_artifact_precheck = PASS',flush=True)
'@
& $Python -u -c $Precheck $C175Summary $C174Summary
if ($LASTEXITCODE -ne 0) { throw "C176 source/artifact precheck failed" }
$Regression = @'
from pathlib import Path
import sys,unittest
from fold_lm.v05_benchmarks import gate_e_c176_conditional_loss as b
names=b.regression_modules(Path.cwd())
assert len(names)==len(set(names))==60
suite=unittest.defaultTestLoader.loadTestsFromNames(names)
assert suite.countTestCases()==1001,f'Expected1001 tests, got{suite.countTestCases()}'
r=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if r.wasSuccessful() else 1)
'@
$Out = Join-Path $Root ("runs\c176-v5e-conditional-loss-" + [guid]::NewGuid().ToString("N"))
$Completed = $false
try {
    Write-Output "=== focused regression ==="
    & $Python -u -c $Regression
    if ($LASTEXITCODE -ne 0) { throw "C176 regression failed; do not start training" }
    Confirm-Repository
    & $Python -u -m fold_lm.v05_benchmarks.gate_e_c176_conditional_loss `
        --c175-summary $C175Summary --c174-summary $C174Summary --output-dir $Out --expected-head $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C176 execution failed; preserve invalid.json" }
    $Postcheck = @'
from pathlib import Path
import sys
from fold_lm.v05_benchmarks import gate_e_c176_conditional_loss as b
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
out=Path(sys.argv[1]);b.precheck(Path(sys.argv[2]),Path(sys.argv[3]),Path.cwd())
p=audit.read_json(out/'summary.json')
assert p['experiment_id']==b.EXPERIMENT_ID and p['commit_sha']==sys.argv[4]
assert p['diagnostic_execution_valid'] is True and p['status'] in ('PASS','FAIL')
assert p['trained_models']==6 and p['fresh_seeds']==3 and len(p['fit_records'])==6
assert [(r['seed'],r['arm']) for r in p['fit_records']]==[(s,a) for s in b.SEEDS for a in b.ARMS]
assert all(r['steps']==2000 and r['examples_drawn']==512000 for r in p['fit_records'])
assert p['training_steps_total']==12000 and p['training_examples_drawn']==3072000
assert p['pilot_predictions']==56376 and p['training_resubstitution_predictions']==254664
assert p['inference_forward_calls']==312 and p['historical_checkpoint_deserializations']==0
assert len(p['source_blobs'])==52 and len(p['input_sha256'])==71
for name,want in p['input_sha256'].items():assert audit.sha(name)==want,name
expected={'conditional-plan.json','train-weight-table.json','pilot-predictions.json','training-predictions.npz'}
expected|={f'probe-{s}-{a}.pt' for s in b.SEEDS for a in b.ARMS}
assert len(p['artifacts'])==10 and {a['file'] for a in p['artifacts']}==expected
for a in p['artifacts']:
    f=audit.safe_child(out,a['file'])
    assert audit.sha(f)==a['sha256'] and f.stat().st_size==a['serialized_bytes'],str(f)
assert ('PASS' if b.gate(p['pairs']) else 'FAIL')==p['status']
print('summary =',out/'summary.json')
print('summary_sha256 =',audit.sha(out/'summary.json'))
print('scientific_status =',p['status'])
'@
    & $Python -u -c $Postcheck $Out $C175Summary $C174Summary $ExpectedHead
    if ($LASTEXITCODE -ne 0) { throw "C176 artifact postcheck failed" }
    $Completed = $true
}
finally {
    Write-Output "=== C176 POSTCHECK ==="
    Confirm-Repository
    Write-Output "protected_inputs = preserved; tracked_tree = clean; execution_HEAD = preserved"
    Write-Output "run_execution_valid = $Completed"
}
