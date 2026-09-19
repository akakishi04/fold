param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference="Stop"
$PSNativeCommandUseErrorActionPreference=$false
Set-StrictMode -Version Latest
$Root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$log=Join-Path $Root "runs\chatgpt-last.log"

$runArgs=@{
 ExpectedHead=$ExpectedHead
 C194Summary=(Join-Path $Root "runs\c194-v5e-generic-loop-8bc090e9457a4a3085b00fa79ab0831a\summary.json")
 C193Summary=(Join-Path $Root "runs\c193-v5e-budget13-closure-ddc6bbafaddb4836aa1db16a3ea08211\summary.json")
 C192Summary=(Join-Path $Root "runs\c192-v5e-post3-shadow-ca96332ef4a4443abc566a4aadd52141\summary.json")
 C191Summary=(Join-Path $Root "runs\c191-v5e-third-acquisition-85be544455144f10965cbd9ee0c1c59e\summary.json")
 C190Summary=(Join-Path $Root "runs\c190-v5e-iterative-multimissing-fce03e62811c4166a11280c32ecfc534\summary.json")
 C189Summary=(Join-Path $Root "runs\c189-v5e-live-multimissing-target-19ae6f0a2dd8402492df6beab82dc3a3\summary.json")
 C188Summary=(Join-Path $Root "runs\c188-v5e-multimissing-target-selection-81830a0e8ba741519c9172bdf2f7a7bc\summary.json")
 C187Summary=(Join-Path $Root "runs\c187-v5e-restricted-acquisition-cc3717a5a9994142a9147953dce83573\summary.json")
 C186Summary=(Join-Path $Root "runs\c186-v5e-nonadmission-0d274f54409144cf83899758d020e82b\summary.json")
 C185Summary=(Join-Path $Root "runs\c185-v5e-single-missing-acquisition-72d30a1a4e114de5b981352de26055e6\summary.json")
 C184Summary=(Join-Path $Root "runs\c184-v5e-canonical-indices-5e2a159b64164b3a919762ebdbdc4f90\summary.json")
 C183Summary=(Join-Path $Root "runs\c183-v5e-path-attribution-b806a83c1a4044538713b844fe640198\summary.json")
 C182Summary=(Join-Path $Root "runs\c182-v5e-frozen-renaming-fa52ca6c8c9042598deeee261ca6e8c4\summary.json")
 C181Summary=(Join-Path $Root "runs\c181-v5e-internal-semantics-23f8363819474cccb05b0d1ecc8941ad\summary.json")
 C180Summary=(Join-Path $Root "runs\c180-v5e-fact-bypass-669cce9093064995bf26b1bf176dd609\summary.json")
 C179Summary=(Join-Path $Root "runs\c179-v5e-shared-graph-49f8f07577d74b8dace13a677691fe99\summary.json")
 C178Summary=(Join-Path $Root "runs\c178-v5e-leaf-binding-e16d745f5b3242728e9c561023938719\summary.json")
 C177Summary=(Join-Path $Root "runs\c177-v5e-score-order-c18e0ed086f34e0aada4635e907e470f\summary.json")
 C176Summary=(Join-Path $Root "runs\c176-v5e-conditional-loss-baeba02034ff414094cfd5a25da5d9b7\summary.json")
 C174Summary=(Join-Path $Root "runs\c174-v5e-learned-necessity-529b2018ef2a4a568a30fdb89b662410\summary.json")
}
$failure=$null
try{
 & {
   Write-Output "=== C195 repository preflight ==="
   $branch=git branch --show-current
   if($LASTEXITCODE -ne 0 -or $branch -ne "feat/sft-target-loss"){throw "Unexpected branch: $branch"}
   $dirty=@(git status --porcelain --untracked-files=no)
   if($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0){throw "Tracked working tree is not clean"}
   $head=git rev-parse HEAD
   if($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead){throw "Unexpected synchronized HEAD: $head"}
   .\tools\run_c195.ps1 @runArgs
 } *>&1 | Tee-Object -FilePath $log
}catch{$failure=$_}
finally{
 try{.\tools\publish_experiment_log.ps1 -ExperimentId C195 -LogPath $log -ExecutionHead $ExpectedHead}
 catch{
   if($null -ne $failure){throw "C195 execution failed and log publication also failed. Execution error: $($failure.Exception.Message); publish error: $($_.Exception.Message)"}
   throw
 }
}
if($null -ne $failure){throw $failure}
