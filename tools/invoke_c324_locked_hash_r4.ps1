param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
function Skip-Invocation {
    param([string]$Reason)
    Write-Output "invocation_skipped = $Reason"
    Write-Output 'experiment_executed = False'
    Write-Output 'execution_log_publish_attempted = False'
}
if ($PSVersionTable.PSEdition -ne 'Core' -or $PSVersionTable.PSVersion -lt [version]'7.3') { Skip-Invocation 'POWERSHELL_7_3_REQUIRED'; return }
$PSNativeCommandArgumentPassing = 'Standard'
$branch = git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branch -ne 'feat/sft-target-loss') { Skip-Invocation 'WRONG_BRANCH'; return }
$head = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead) { Skip-Invocation 'STALE_EXPECTED_HEAD'; return }
$dirty = @(git status --porcelain --untracked-files=no)
if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { Skip-Invocation 'DIRTY_TRACKED_TREE'; return }
$handoff = Get-Content -LiteralPath (Join-Path $Root 'docs\experiment-ledger-and-handoff.md') -Raw -Encoding UTF8
$formal = [regex]::Match($handoff,'(?ms)^## Formal state\s+(?<body>.*?)(?=^## |\z)')
$body = $formal.Groups['body'].Value
if (-not $formal.Success -or $body -notmatch 'C324 ACTIVE / INVALID ATTEMPT RECOVERY' -or $body -notmatch '(?m)^recovery_action = LOCKED_HASH_R4\s*$') { Skip-Invocation 'STALE_RECOVERY'; return }
$Python = Join-Path $Root '.venv-py31315\Scripts\python.exe'
$Script = Join-Path $Root 'tools\c324_locked_hash_r4.py'
if (-not (Test-Path -LiteralPath $Python -PathType Leaf) -or -not (Test-Path -LiteralPath $Script -PathType Leaf)) { Skip-Invocation 'DIAGNOSTIC_DEPENDENCY_MISSING'; return }
New-Item -ItemType Directory -Path (Join-Path $Root 'runs') -Force | Out-Null
$id = [guid]::NewGuid().ToString('N')
$log = Join-Path $Root ('runs\c324-locked-hash-r4-' + $id + '.log')
$out = Join-Path $Root ('runs\c324-locked-hash-r4-' + $id)
$failure = $null
try {
    & {
        Write-Output 'execution_role = C324-R4-LOCKED-HASH-QUALIFICATION'
        Write-Output 'scientific_execution_requested = False'
        Write-Output "diagnostic_execution_head = $ExpectedHead"
        & $Python -B -X faulthandler -u $Script --expected-head $ExpectedHead --output-dir $out
        if ($LASTEXITCODE -ne 0) { throw "C324 R4 qualification controller failed: $LASTEXITCODE" }
    } *>&1 | Tee-Object -FilePath $log
}
catch { $failure = $_ }
finally {
    try { .\tools\publish_experiment_log.ps1 -ExperimentId C324 -LogPath $log -ExecutionHead $ExpectedHead }
    catch {
        if ($null -ne $failure) { throw "C324 qualification and publication failed: $($failure.Exception.Message); $($_.Exception.Message)" }
        throw
    }
}
if ($null -ne $failure) { throw $failure }
