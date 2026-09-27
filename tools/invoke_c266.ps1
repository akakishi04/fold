param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$log = Join-Path $Root "runs\chatgpt-last.log"
function Skip-Invocation {
    param([string]$Reason)
    Write-Output "invocation_skipped = $Reason"
    Write-Output "experiment_executed = False"
    Write-Output "execution_log_publish_attempted = False"
}
$branchNow = git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branchNow -ne "feat/sft-target-loss") { Skip-Invocation "WRONG_BRANCH"; return }
$dirty = @(git status --porcelain --untracked-files=no)
if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { Skip-Invocation "DIRTY_TRACKED_TREE"; return }
$headNow = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $headNow -ne $ExpectedHead) { Skip-Invocation "STALE_EXPECTED_HEAD"; return }
$handoffPath = Join-Path $Root "docs\experiment-ledger-and-handoff.md"
if (-not (Test-Path -LiteralPath $handoffPath -PathType Leaf)) { Skip-Invocation "HANDOFF_MISSING"; return }
$handoff = Get-Content -LiteralPath $handoffPath -Raw -Encoding UTF8
$formal = [regex]::Match($handoff, '(?ms)^## Formal state\s+(?<body>.*?)(?=^## |\z)')
if (-not $formal.Success) { Skip-Invocation "FORMAL_STATE_UNRESOLVED"; return }
$active = [regex]::Matches($formal.Groups["body"].Value, 'C(?<id>\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)')
if ($active.Count -ne 1 -or $active[0].Groups["id"].Value -ne "266") { Skip-Invocation "STALE_EXPERIMENT"; return }
$runnerPath = Join-Path $Root "tools\run_c266.ps1"
$runnerTokens = $null
$runnerParseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($runnerPath,[ref]$runnerTokens,[ref]$runnerParseErrors) | Out-Null
if ($runnerParseErrors.Count -gt 0) { Skip-Invocation "RUNNER_PARSE_ERROR"; return }
$runArgs = @{
    ExpectedHead = $ExpectedHead
    C265Summary = (Join-Path $Root "runs\c265-v5b-identifiers-755ab6d49ab84080ac18ff8f0699953f\summary.json")
    C264Summary = (Join-Path $Root "runs\c264-v5b-two-fact-46c2297b66ba41a9b8f66f7bfca48935\summary.json")
    C263Summary = (Join-Path $Root "runs\c263-v5b-rate-order-638f26dfee354c9cb3aa5fa174d3e9f6\summary.json")
}
$failure = $null
try {
    & {
        Write-Output "=== C266 repository preflight ==="
        Write-Output "execution_head = $headNow"
        .\tools\run_c266.ps1 @runArgs
    } *>&1 | Tee-Object -FilePath $log
}
catch { $failure = $_ }
finally {
    try { .\tools\publish_experiment_log.ps1 -ExperimentId C266 -LogPath $log -ExecutionHead $ExpectedHead }
    catch {
        if ($null -ne $failure) { throw "C266 execution and publication failed: $($failure.Exception.Message); $($_.Exception.Message)" }
        throw
    }
}
if ($null -ne $failure) { throw $failure }
