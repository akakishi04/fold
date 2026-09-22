param(
    [Parameter(Mandatory=$true)][string]$ExpectedHead
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$log = Join-Path $Root "runs\chatgpt-last.log"
$ExperimentId = "C219"
$Branch = "feat/sft-target-loss"

function Skip-Invocation {
    param([Parameter(Mandatory=$true)][string]$Reason,[string]$Detail = "")
    Write-Output "=== $ExperimentId invocation skipped ==="
    Write-Output "invocation_skipped = $Reason"
    if (-not [string]::IsNullOrWhiteSpace($Detail)) { Write-Output "detail = $Detail" }
    Write-Output "experiment_executed = False"
    Write-Output "execution_log_publish_attempted = False"
}

$branchNow = git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branchNow -ne $Branch) { Skip-Invocation -Reason "WRONG_BRANCH" -Detail "expected=$Branch actual=$branchNow"; return }
$dirty = @(git status --porcelain --untracked-files=no)
if ($LASTEXITCODE -ne 0) { Skip-Invocation -Reason "GIT_STATUS_FAILED"; return }
if ($dirty.Count -gt 0) { Skip-Invocation -Reason "DIRTY_TRACKED_TREE"; return }
$headNow = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { Skip-Invocation -Reason "HEAD_LOOKUP_FAILED"; return }
if ($headNow -ne $ExpectedHead) { Skip-Invocation -Reason "STALE_EXPECTED_HEAD" -Detail "expected=$ExpectedHead current=$headNow"; return }

$handoffPath = Join-Path $Root "docs\experiment-ledger-and-handoff.md"
if (-not (Test-Path -LiteralPath $handoffPath -PathType Leaf)) { Skip-Invocation -Reason "HANDOFF_MISSING"; return }
$handoff = Get-Content -LiteralPath $handoffPath -Raw -Encoding UTF8
$formalMatch = [regex]::Match($handoff, '(?ms)^## Formal state\s+(?<body>.*?)(?=^## |\z)')
if (-not $formalMatch.Success) { Skip-Invocation -Reason "FORMAL_STATE_UNRESOLVED"; return }
$activeMatch = [regex]::Match($formalMatch.Groups["body"].Value, 'C(?<id>\d{3}) ACTIVE / (?<state>NOT YET JUDGED|INVALID ATTEMPT RECOVERY)')
if (-not $activeMatch.Success -or $activeMatch.Groups["id"].Value -ne "219") {
    $active = if ($activeMatch.Success) { "C" + $activeMatch.Groups["id"].Value } else { "UNRESOLVED" }
    Skip-Invocation -Reason "STALE_EXPERIMENT" -Detail "requested=C219 active=$active"
    return
}

$runnerPath = Join-Path $Root "tools\run_c219.ps1"
$runnerTokens = $null
$runnerParseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($runnerPath,[ref]$runnerTokens,[ref]$runnerParseErrors) | Out-Null
if ($runnerParseErrors.Count -gt 0) {
    $detail = ($runnerParseErrors | ForEach-Object { $_.Message }) -join " | "
    Skip-Invocation -Reason "RUNNER_PARSE_ERROR" -Detail $detail
    return
}

$runArgs = @{
    ExpectedHead = $ExpectedHead
    C218Summary = (Join-Path $Root "runs\c218-v5f-learned-writer-7ccc565edaba498c9af8f7caea7d17a4\summary.json")
}

$failure = $null
try {
    & {
        Write-Output "=== C219 repository preflight ==="
        Write-Output "branch = $branchNow"
        Write-Output "execution_head = $headNow"
        .\tools\run_c219.ps1 @runArgs
    } *>&1 | Tee-Object -FilePath $log
}
catch { $failure = $_ }
finally {
    try { .\tools\publish_experiment_log.ps1 -ExperimentId C219 -LogPath $log -ExecutionHead $ExpectedHead }
    catch {
        if ($null -ne $failure) {
            throw "C219 execution failed and log publication also failed. Execution error: $($failure.Exception.Message); publish error: $($_.Exception.Message)"
        }
        throw
    }
}
if ($null -ne $failure) { throw $failure }
