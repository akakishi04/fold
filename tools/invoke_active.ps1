param(
    [Parameter(Mandatory=$true)][string]$ExpectedHead
)
$ErrorActionPreference="Stop"
$PSNativeCommandUseErrorActionPreference=$false
Set-StrictMode -Version Latest

$Root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Branch="feat/sft-target-loss"

function Skip-Invocation {
    param(
        [Parameter(Mandatory=$true)][string]$Reason,
        [string]$Detail=""
    )
    Write-Output "=== FOLD experiment invocation skipped ==="
    Write-Output "invocation_skipped = $Reason"
    if(-not [string]::IsNullOrWhiteSpace($Detail)){
        Write-Output "detail = $Detail"
    }
    Write-Output "experiment_executed = False"
    Write-Output "execution_log_publish_attempted = False"
}

$actualBranch=git branch --show-current
if($LASTEXITCODE -ne 0 -or $actualBranch -ne $Branch){
    Skip-Invocation -Reason "WRONG_BRANCH" -Detail "expected=$Branch actual=$actualBranch"
    return
}

$dirty=@(git status --porcelain --untracked-files=no)
if($LASTEXITCODE -ne 0){
    Skip-Invocation -Reason "GIT_STATUS_FAILED"
    return
}
if($dirty.Count -gt 0){
    Skip-Invocation -Reason "DIRTY_TRACKED_TREE"
    return
}

$currentHead=git rev-parse HEAD
if($LASTEXITCODE -ne 0){
    Skip-Invocation -Reason "HEAD_LOOKUP_FAILED"
    return
}
if($currentHead -ne $ExpectedHead){
    Skip-Invocation -Reason "STALE_EXPECTED_HEAD" -Detail "expected=$ExpectedHead current=$currentHead"
    return
}

$handoffPath=Join-Path $Root "docs\experiment-ledger-and-handoff.md"
if(-not(Test-Path -LiteralPath $handoffPath -PathType Leaf)){
    Skip-Invocation -Reason "HANDOFF_MISSING"
    return
}
$handoff=Get-Content -LiteralPath $handoffPath -Raw -Encoding UTF8

$matches=[regex]::Matches(
    $handoff,
    '(?m)^\*\*[^*\r\n]*C(?<id>\d{3}) ACTIVE / (?<state>NOT YET JUDGED|INVALID ATTEMPT RECOVERY)[^*\r\n]*\*\*
if($matches.Count -ne 1){
    Skip-Invocation -Reason "ACTIVE_EXPERIMENT_UNRESOLVED" -Detail "matches=$($matches.Count)"
    return
}

$activeExperiment="C"+$matches[0].Groups["id"].Value
$launcher=Join-Path $Root ("tools\invoke_"+$activeExperiment.ToLowerInvariant()+".ps1")
if(-not(Test-Path -LiteralPath $launcher -PathType Leaf)){
    Skip-Invocation -Reason "ACTIVE_LAUNCHER_MISSING" -Detail "active=$activeExperiment"
    return
}

Write-Output "=== FOLD active experiment dispatcher ==="
Write-Output "active_experiment = $activeExperiment"
Write-Output "expected_head = $ExpectedHead"
Write-Output "current_head = $currentHead"
Write-Output "launcher = $launcher"

& $launcher -ExpectedHead $ExpectedHead
if($LASTEXITCODE -ne 0){
    exit $LASTEXITCODE
}

)
if($matches.Count -ne 1){
    Skip-Invocation -Reason "ACTIVE_EXPERIMENT_UNRESOLVED" -Detail "matches=$($matches.Count)"
    return
}

$activeExperiment="C"+$matches[0].Groups["id"].Value
$launcher=Join-Path $Root ("tools\invoke_"+$activeExperiment.ToLowerInvariant()+".ps1")
if(-not(Test-Path -LiteralPath $launcher -PathType Leaf)){
    Skip-Invocation -Reason "ACTIVE_LAUNCHER_MISSING" -Detail "active=$activeExperiment"
    return
}

Write-Output "=== FOLD active experiment dispatcher ==="
Write-Output "active_experiment = $activeExperiment"
Write-Output "expected_head = $ExpectedHead"
Write-Output "current_head = $currentHead"
Write-Output "launcher = $launcher"

& $launcher -ExpectedHead $ExpectedHead
if($LASTEXITCODE -ne 0){
    exit $LASTEXITCODE
}
