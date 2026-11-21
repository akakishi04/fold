param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference="Stop"
$PSNativeCommandUseErrorActionPreference=$false
Set-StrictMode -Version Latest
$Root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$log=Join-Path $Root "runs\chatgpt-last.log"

$runArgs=@{
 ExpectedHead=$ExpectedHead
 C200Summary=(Join-Path $Root "runs\c200-v5e-acquisition-channel-input-d892b01c24ee49cfbb87758e7a208be0\summary.json")
 C199Summary=(Join-Path $Root "runs\c199-v5e-attempt-limit-886ac50bbbe046ebba61316e6bf97268\summary.json")
}

$failure=$null
try{
 & {
   Write-Output "=== C201 repository preflight ==="
   $branch=git branch --show-current
   if($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss"){throw "Unexpected branch: $branch"}
   $dirty=@(git status --porcelain --untracked-files=no)
   if($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0){throw "Tracked working tree is not clean"}
   $head=git rev-parse HEAD
   if($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead){throw "Unexpected synchronized HEAD: $head"}
   .\tools\run_c201.ps1 @runArgs
 } *>&1 | Tee-Object -FilePath $log
}catch{$failure=$_}
finally{
 try{.\tools\publish_experiment_log.ps1 -ExperimentId C201 -LogPath $log -ExecutionHead $ExpectedHead}
 catch{
   if($null -ne $failure){throw "C201 execution failed and log publication also failed. Execution error: $($failure.Exception.Message); publish error: $($_.Exception.Message)"}
   throw
 }
}
if($null -ne $failure){throw $failure}
