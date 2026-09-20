param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference="Stop"
$PSNativeCommandUseErrorActionPreference=$false
Set-StrictMode -Version Latest
$Root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$log=Join-Path $Root "runs\chatgpt-last.log"

$runArgs=@{
 ExpectedHead=$ExpectedHead
 C203Summary=(Join-Path $Root "runs\c203-v5e-mixed-channel-multistep-f8a35e95871341ddafa1a273aed80cfb\summary.json")
 C202Summary=(Join-Path $Root "runs\c202-v5e-three-channel-dispatch-4c36064e0e7b4b87a8deb9714cb6aa66\summary.json")
 C201Summary=(Join-Path $Root "runs\c201-v5e-selected-fact-channel-route-37e1d67baaff4cd7a67addeb75da0aca\summary.json")
 C200Summary=(Join-Path $Root "runs\c200-v5e-acquisition-channel-input-d892b01c24ee49cfbb87758e7a208be0\summary.json")
 C199Summary=(Join-Path $Root "runs\c199-v5e-attempt-limit-886ac50bbbe046ebba61316e6bf97268\summary.json")
 C174Summary=(Join-Path $Root "runs\c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410\summary.json")
 C181Summary=(Join-Path $Root "runs\c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad\summary.json")
 C188Summary=(Join-Path $Root "runs\c188-v5e-multimissing-target-selection-81830a0e8ba741519c9172bdf2f7a7bc\summary.json")
}

$failure=$null
try{
 & {
   Write-Output "=== C204 repository preflight ==="
   $branch=git branch --show-current
   if($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss"){throw "Unexpected branch: $branch"}
   $dirty=@(git status --porcelain --untracked-files=no)
   if($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0){throw "Tracked working tree is not clean"}
   $head=git rev-parse HEAD
   if($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead){throw "Unexpected synchronized HEAD: $head"}
   .\tools\run_c204.ps1 @runArgs
 } *>&1 | Tee-Object -FilePath $log
}catch{$failure=$_}
finally{
 try{.\tools\publish_experiment_log.ps1 -ExperimentId C204 -LogPath $log -ExecutionHead $ExpectedHead}
 catch{
   if($null -ne $failure){throw "C204 execution failed and log publication also failed. Execution error: $($failure.Exception.Message); publish error: $($_.Exception.Message)"}
   throw
 }
}
if($null -ne $failure){throw $failure}
