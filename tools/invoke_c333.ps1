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
$activeEntries = [regex]::Matches($formal.Groups['body'].Value,'C(?<id>\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)')
if (-not $formal.Success -or $activeEntries.Count -ne 1 -or $activeEntries[0].Groups['id'].Value -ne '333') { Skip-Invocation 'STALE_EXPERIMENT'; return }
$Python = Join-Path $Root '.venv-py31315\Scripts\python.exe'
$Script = Join-Path $Root 'tools\c333_execution.py'
$Runner = Join-Path $Root 'tools\run_c333.ps1'
foreach ($path in @($Python,$Script,$Runner)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { Skip-Invocation 'DEPENDENCY_MISSING'; return }
}
foreach ($path in @($PSCommandPath,$Runner)) {
    $tokens = $null; $errors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($path,[ref]$tokens,[ref]$errors) | Out-Null
    if ($errors.Count -gt 0) { Skip-Invocation 'LAUNCHER_OR_RUNNER_PARSE_ERROR'; return }
}
New-Item -ItemType Directory -Path (Join-Path $Root 'runs') -Force | Out-Null
$id = [guid]::NewGuid().ToString('N')
$log = Join-Path $Root ('runs\c333-paired-localization-' + $id + '.log')
$folder = Join-Path $Root ('runs\c333-paired-localization-' + $id)
$failure = $null
try {
    & {
        Write-Output 'execution_role = C333-PAIRED-GATE-LOCALIZATION'
        Write-Output 'scientific_execution_requested = True'
        Write-Output 'scientific_training_requested = False'
        Write-Output "scientific_execution_head = $ExpectedHead"
        & $Runner -ExpectedHead $ExpectedHead -Folder $folder
    } *>&1 | Tee-Object -FilePath $log
}
catch { $failure = $_ }
finally {
    try { .\tools\publish_experiment_log.ps1 -ExperimentId C333 -LogPath $log -ExecutionHead $ExpectedHead }
    catch {
        if ($null -ne $failure) { throw "C333 execution and publication failed: $($failure.Exception.Message); $($_.Exception.Message)" }
        throw
    }
}
if ($null -ne $failure) { throw $failure }
