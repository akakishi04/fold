param(
    [Parameter(Mandatory=$true)][string]$ExpectedHead
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Branch = "feat/sft-target-loss"

function Skip-Invocation {
    param(
        [Parameter(Mandatory=$true)][string]$Reason,
        [string]$Detail = ""
    )
    Write-Output "=== FOLD experiment invocation skipped ==="
    Write-Output "invocation_skipped = $Reason"
    if (-not [string]::IsNullOrWhiteSpace($Detail)) {
        Write-Output "detail = $Detail"
    }
    Write-Output "experiment_executed = False"
    Write-Output "execution_log_publish_attempted = False"
}

function Report-PublishedResult {
    param(
        [Parameter(Mandatory=$true)][string]$ExperimentId,
        [Parameter(Mandatory=$true)][string]$ExecutionHead,
        [Parameter(Mandatory=$true)][string]$CurrentHead,
        [Parameter(Mandatory=$true)][string]$MetadataPath
    )
    Write-Output "=== FOLD experiment result already published ==="
    Write-Output "invocation_status = RESULT_ALREADY_PUBLISHED"
    Write-Output "active_experiment = $ExperimentId"
    Write-Output "execution_head = $ExecutionHead"
    Write-Output "current_head = $CurrentHead"
    Write-Output "published_metadata = $MetadataPath"
    Write-Output "experiment_executed = False"
    Write-Output "execution_log_publish_attempted = False"
    Write-Output "action = Do not rerun this experiment; send the completion result for judgment."
}

$actualBranch = git branch --show-current
if ($LASTEXITCODE -ne 0 -or $actualBranch -ne $Branch) {
    Skip-Invocation -Reason "WRONG_BRANCH" -Detail "expected=$Branch actual=$actualBranch"
    return
}

$dirty = @(git status --porcelain --untracked-files=no)
if ($LASTEXITCODE -ne 0) {
    Skip-Invocation -Reason "GIT_STATUS_FAILED"
    return
}
if ($dirty.Count -gt 0) {
    Skip-Invocation -Reason "DIRTY_TRACKED_TREE"
    return
}

$currentHead = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) {
    Skip-Invocation -Reason "HEAD_LOOKUP_FAILED"
    return
}
$handoffPath = Join-Path $Root "docs\experiment-ledger-and-handoff.md"
if (-not (Test-Path -LiteralPath $handoffPath -PathType Leaf)) {
    Skip-Invocation -Reason "HANDOFF_MISSING"
    return
}
$handoff = Get-Content -LiteralPath $handoffPath -Raw -Encoding UTF8

$formalPattern = '(?ms)^## Formal state\s+(?<body>.*?)(?=^## |\z)'
$formalMatch = [regex]::Match($handoff, $formalPattern)
if (-not $formalMatch.Success) {
    Skip-Invocation -Reason "FORMAL_STATE_UNRESOLVED"
    return
}
$activePattern = 'C(?<id>\d{3}) ACTIVE / (?<state>NOT YET JUDGED|INVALID ATTEMPT RECOVERY)'
$activeMatches = [regex]::Matches($formalMatch.Groups["body"].Value, $activePattern)
if ($activeMatches.Count -ne 1) {
    Skip-Invocation -Reason "ACTIVE_EXPERIMENT_UNRESOLVED" -Detail "matches=$($activeMatches.Count)"
    return
}

$activeExperiment = "C" + $activeMatches[0].Groups["id"].Value

# A scientific attempt publishes latest.json in a later log-only commit.
# If its execution_head matches this command's ExpectedHead, the run already happened.
# Report that benign state instead of mislabeling the published log commit as stale.
if ($currentHead -ne $ExpectedHead) {
    $publishedMetadataPath = Join-Path $Root ("docs\experiment-run-logs\" + $activeExperiment.ToLowerInvariant() + "\latest.json")
    if (Test-Path -LiteralPath $publishedMetadataPath -PathType Leaf) {
        try {
            $publishedMetadata = Get-Content -LiteralPath $publishedMetadataPath -Raw -Encoding UTF8 | ConvertFrom-Json
            if (
                $publishedMetadata.experiment_id -eq $activeExperiment -and
                $publishedMetadata.execution_head -eq $ExpectedHead
            ) {
                Report-PublishedResult -ExperimentId $activeExperiment -ExecutionHead $ExpectedHead -CurrentHead $currentHead -MetadataPath $publishedMetadataPath
                return
            }
        }
        catch {
            # Metadata parse failure must not weaken the normal stale-head safety stop.
        }
    }

    Skip-Invocation -Reason "STALE_EXPECTED_HEAD" -Detail "expected=$ExpectedHead current=$currentHead"
    return
}
$launcher = Join-Path $Root ("tools\invoke_" + $activeExperiment.ToLowerInvariant() + ".ps1")
if (-not (Test-Path -LiteralPath $launcher -PathType Leaf)) {
    Skip-Invocation -Reason "ACTIVE_LAUNCHER_MISSING" -Detail "active=$activeExperiment"
    return
}

# Parse the selected launcher before invoking it. A syntax error is an operational skip.
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile(
    $launcher,
    [ref]$tokens,
    [ref]$parseErrors
) | Out-Null
if ($parseErrors.Count -gt 0) {
    $detail = ($parseErrors | ForEach-Object { $_.Message }) -join " | "
    Skip-Invocation -Reason "ACTIVE_LAUNCHER_PARSE_ERROR" -Detail $detail
    return
}

Write-Output "=== FOLD active experiment dispatcher ==="
Write-Output "active_experiment = $activeExperiment"
Write-Output "expected_head = $ExpectedHead"
Write-Output "current_head = $currentHead"
Write-Output "launcher = $launcher"

& $launcher -ExpectedHead $ExpectedHead
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
