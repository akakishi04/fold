param(
    [Parameter(Mandatory = $true)][ValidatePattern('^C\d{3}$')][string]$ExperimentId,
    [Parameter(Mandatory = $true)][string]$LogPath,
    [Parameter(Mandatory = $true)][string]$ExecutionHead,
    [string]$Branch = "feat/sft-target-loss"
)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root

$actualBranch = git branch --show-current
if ($LASTEXITCODE -ne 0 -or $actualBranch -ne $Branch) {
    throw "Unexpected branch before log publish: $actualBranch"
}
$origin = git remote get-url origin
if ($LASTEXITCODE -ne 0 -or $origin -notmatch '[:/]akakishi04/fold(?:\.git)?$') {
    throw "Unexpected origin before log publish: $origin"
}
$head = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $head -ne $ExecutionHead) {
    throw "Execution HEAD changed before log publish: $head"
}
$dirtyTracked = @(git status --porcelain --untracked-files=no)
if ($LASTEXITCODE -ne 0 -or $dirtyTracked.Count -gt 0) {
    throw "Tracked tree must be clean before publishing the execution log"
}
git diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    throw "Pre-existing staged changes are not allowed"
}
if ($LASTEXITCODE -notin @(0,1)) {
    throw "Unable to inspect staged changes"
}

$resolvedLog = (Resolve-Path -LiteralPath $LogPath -ErrorAction Stop).Path
$runsRoot = [IO.Path]::GetFullPath((Join-Path $Root "runs")) + [IO.Path]::DirectorySeparatorChar
$fullLog = [IO.Path]::GetFullPath($resolvedLog)
if (-not $fullLog.StartsWith($runsRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Only logs under the ignored runs/ directory may be published"
}
$info = Get-Item -LiteralPath $fullLog
if ($info.Length -le 0 -or $info.Length -gt 10MB) {
    throw "Execution log must be nonempty and <= 10 MiB"
}
# Validate UTF-8 text before creating tracked documentation.
$text = Get-Content -LiteralPath $fullLog -Raw -Encoding UTF8 -ErrorAction Stop
if ([string]::IsNullOrWhiteSpace($text)) {
    throw "Execution log is empty text"
}

$dir = Join-Path $Root ("docs\experiment-run-logs\" + $ExperimentId.ToLowerInvariant())
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$dest = Join-Path $dir "latest.log"
$meta = Join-Path $dir "latest.json"
Copy-Item -LiteralPath $fullLog -Destination $dest -Force

$sha = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant()
$metadata = [ordered]@{
    schema = "fold-experiment-run-log-v1"
    experiment_id = $ExperimentId
    execution_head = $ExecutionHead
    log_sha256 = $sha
    log_bytes = (Get-Item -LiteralPath $dest).Length
}
$metadata | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $meta -Encoding utf8NoBOM

git add -- $dest $meta
if ($LASTEXITCODE -ne 0) {
    throw "git add failed for execution log"
}
$allowed = @(
    ("docs/experiment-run-logs/" + $ExperimentId.ToLowerInvariant() + "/latest.log"),
    ("docs/experiment-run-logs/" + $ExperimentId.ToLowerInvariant() + "/latest.json")
)
$staged = @(git diff --cached --name-only)
if ($LASTEXITCODE -ne 0) {
    throw "Unable to inspect staged log files"
}
if ($staged.Count -eq 0) {
    Write-Output "execution_log_publish = unchanged"
    Write-Output "execution_log_sha256 = $sha"
    exit 0
}
if (@($staged | Where-Object { $_ -notin $allowed }).Count -gt 0) {
    throw "Unexpected staged path during log publication: $($staged -join ', ')"
}

git commit -m "logs(fold): publish $ExperimentId execution log"
if ($LASTEXITCODE -ne 0) {
    throw "Execution log commit failed"
}
$logCommit = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) {
    throw "Unable to read execution log commit"
}
git push origin $Branch
if ($LASTEXITCODE -ne 0) {
    throw "Execution log push failed; local commit retained: $logCommit"
}
Write-Output "execution_log_publish = PASS"
Write-Output "execution_log_commit = $logCommit"
Write-Output "execution_log_path = $($allowed[0])"
Write-Output "execution_log_sha256 = $sha"
