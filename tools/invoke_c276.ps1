param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$log = Join-Path $Root "runs\chatgpt-last.log"
$preflightLog = Join-Path $Root "runs\c276-preflight-last.log"

function Skip-Invocation {
    param([string]$Reason,[string]$Detail="")
    Write-Output "invocation_skipped = $Reason"
    if (-not [string]::IsNullOrWhiteSpace($Detail)) { Write-Output "detail = $Detail" }
    Write-Output "experiment_executed = False"
    Write-Output "execution_log_publish_attempted = False"
}

if ($PSVersionTable.PSEdition -ne "Core" -or $PSVersionTable.PSVersion -lt [version]"7.3") {
    Skip-Invocation "POWERSHELL_7_3_REQUIRED"; return
}
$PSNativeCommandArgumentPassing = "Standard"

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
$active = [regex]::Matches($formal.Groups["body"].Value, 'C(?<id>\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY|NOT YET JUDGED \(PREFLIGHT RECOVERY\))')
if ($active.Count -ne 1 -or $active[0].Groups["id"].Value -ne "276") { Skip-Invocation "STALE_EXPERIMENT"; return }

$runnerPath = Join-Path $Root "tools\run_c276.ps1"
$runnerTokens = $null;$runnerParseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($runnerPath,[ref]$runnerTokens,[ref]$runnerParseErrors) | Out-Null
if ($runnerParseErrors.Count -gt 0) { Skip-Invocation "RUNNER_PARSE_ERROR"; return }

$runArgs = @{
    ExpectedHead = $ExpectedHead
    C275Summary = (Join-Path $Root "runs\c275-v5b-gate-failure-audit-fb5be8dc32064545aa7a993b70e50706\summary.json")
    C274Summary = (Join-Path $Root "runs\c274-v5b-directional-boundary-06a7a84bf4554f83b5cb6e099a828178\summary.json")
}

$preflightFailure = $null
try { .\tools\run_c276.ps1 @runArgs -Mode Validate *>&1 | Tee-Object -FilePath $preflightLog }
catch { $preflightFailure = $_ }
if ($null -ne $preflightFailure) {
    Skip-Invocation "AUTHORING_RUNTIME_PREFLIGHT_FAILED" $preflightFailure.Exception.Message
    return
}

$failure = $null
try {
    & {
        Write-Output "=== C276 repository preflight attestation ==="
        Get-Content -LiteralPath $preflightLog -Encoding UTF8
        Write-Output "=== C276 repository scientific execution ==="
        Write-Output "execution_head = $headNow"
        .\tools\run_c276.ps1 @runArgs -Mode Execute
    } *>&1 | Tee-Object -FilePath $log
}
catch { $failure = $_ }
finally {
    try { .\tools\publish_experiment_log.ps1 -ExperimentId C276 -LogPath $log -ExecutionHead $ExpectedHead }
    catch {
        if ($null -ne $failure) { throw "C276 execution and publication failed: $($failure.Exception.Message); $($_.Exception.Message)" }
        throw
    }
}
if ($null -ne $failure) { throw $failure }
