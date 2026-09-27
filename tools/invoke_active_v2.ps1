param(
    [Parameter(Mandatory=$true)][string]$ExpectedHead
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Branch = "feat/sft-target-loss"
$LegacyBlob = "86b5606a5b212b12f416abedac0923da634f88e3"
$LegacyWindowsSha256 = "57a0f1ffa3a9370b5261ec5bf1e9eb3d778dc84f19f35c51e21174f61735a95b"

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

# This is a new, versioned control-plane entry. Never edit the protected legacy entry.
# Return before creating a scientific log when an incompatible host is used.
if ($PSVersionTable.PSEdition -ne "Core" -or $PSVersionTable.PSVersion -lt [version]"7.3") {
    Skip-Invocation -Reason "POWERSHELL_7_3_REQUIRED" -Detail "Use C:\Program Files\PowerShell\7\pwsh.exe"
    return
}
$PSNativeCommandArgumentPassing = "Standard"
$selfTokens = $null
$selfErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$selfTokens,[ref]$selfErrors) | Out-Null
if ($selfErrors.Count -gt 0) {
    Skip-Invocation -Reason "DISPATCHER_PARSE_ERROR"
    return
}

function Report-PublishedResult {
    param([string]$ExperimentId,[string]$ExecutionHead,[string]$CurrentHead)
    Write-Output "=== FOLD experiment result already published ==="
    Write-Output "invocation_status = RESULT_ALREADY_PUBLISHED"
    Write-Output "active_experiment = $ExperimentId"
    Write-Output "execution_head = $ExecutionHead"
    Write-Output "current_head = $CurrentHead"
    Write-Output "experiment_executed = False"
    Write-Output "execution_log_publish_attempted = False"
    Write-Output "action = Inspect the published attempt. Publication does not mean PASS. Do not rerun an old command."
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

if ($currentHead -ne $ExpectedHead) {
    $publishedMetadataPath = Join-Path $Root ("docs\experiment-run-logs\" + $activeExperiment.ToLowerInvariant() + "\latest.json")
    if (Test-Path -LiteralPath $publishedMetadataPath -PathType Leaf) {
        try {
            $publishedMetadata = Get-Content -LiteralPath $publishedMetadataPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $logPath = Join-Path (Split-Path -Parent $publishedMetadataPath) "latest.log"
            if (
                $publishedMetadata.schema -eq "fold-experiment-run-log-v1" -and
                $publishedMetadata.experiment_id -eq $activeExperiment -and
                $publishedMetadata.execution_head -eq $ExpectedHead -and
                (Test-Path -LiteralPath $logPath -PathType Leaf) -and
                (Get-FileHash -LiteralPath $logPath -Algorithm SHA256).Hash.ToLowerInvariant() -eq $publishedMetadata.log_sha256 -and
                (Get-Item -LiteralPath $logPath).Length -eq $publishedMetadata.log_bytes
            ) {
                Report-PublishedResult -ExperimentId $activeExperiment -ExecutionHead $ExpectedHead -CurrentHead $currentHead
                return
            }
        }
        catch {
            # Untrusted/malformed/incomplete publication metadata never authorizes execution.
        }
    }
    Skip-Invocation -Reason "STALE_EXPECTED_HEAD" -Detail "expected=$ExpectedHead current=$currentHead"
    return
}

# Ancestor experiments pin both the Git blob and the original Windows CRLF bytes.
# Verify, never replace expected hashes or rewrite the working file here.
$legacyPath = Join-Path $Root "tools\invoke_active.ps1"
$actualLegacyBlob = git rev-parse "HEAD:tools/invoke_active.ps1"
if ($LASTEXITCODE -ne 0 -or $actualLegacyBlob -ne $LegacyBlob) {
    Skip-Invocation -Reason "LEGACY_DISPATCHER_BLOB_MISMATCH" -Detail "expected=$LegacyBlob actual=$actualLegacyBlob"
    return
}
$actualLegacyHash = (Get-FileHash -LiteralPath $legacyPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualLegacyHash -ne $LegacyWindowsSha256) {
    Skip-Invocation -Reason "LEGACY_DISPATCHER_BYTES_MISMATCH" -Detail "expected=$LegacyWindowsSha256 actual=$actualLegacyHash; check checkout line endings; do not waive parent validation"
    return
}
Write-Output "legacy_dispatcher_pin = PASS"
Write-Output "powershell_host = $($PSVersionTable.PSVersion); native_arguments = Standard"
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
