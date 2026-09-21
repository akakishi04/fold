param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference="Stop";$PSNativeCommandUseErrorActionPreference=$false;Set-StrictMode -Version Latest
$Root=Split-Path -Parent $PSScriptRoot;Set-Location -LiteralPath $Root;$log=Join-Path $Root "runs\chatgpt-last.log"
$ExperimentId="C215";$Branch="feat/sft-target-loss"
function Skip-Invocation { param([string]$Reason,[string]$Detail="");Write-Output "=== $ExperimentId invocation skipped ===";Write-Output "invocation_skipped = $Reason";if($Detail){Write-Output "detail = $Detail"};Write-Output "experiment_executed = False";Write-Output "execution_log_publish_attempted = False" }
$branchNow=git branch --show-current;if($LASTEXITCODE -ne 0 -or $branchNow -ne $Branch){Skip-Invocation "WRONG_BRANCH" "expected=$Branch actual=$branchNow";return}
$dirty=@(git status --porcelain --untracked-files=no);if($LASTEXITCODE -ne 0){Skip-Invocation "GIT_STATUS_FAILED";return};if($dirty.Count -gt 0){Skip-Invocation "DIRTY_TRACKED_TREE";return}
$headNow=git rev-parse HEAD;if($LASTEXITCODE -ne 0){Skip-Invocation "HEAD_LOOKUP_FAILED";return};if($headNow -ne $ExpectedHead){Skip-Invocation "STALE_EXPECTED_HEAD" "expected=$ExpectedHead current=$headNow";return}
$handoffPath=Join-Path $Root "docs\experiment-ledger-and-handoff.md";if(-not(Test-Path $handoffPath -PathType Leaf)){Skip-Invocation "HANDOFF_MISSING";return}
$handoff=Get-Content $handoffPath -Raw -Encoding UTF8;$formalMatch=[regex]::Match($handoff,'(?ms)^## Formal state\s+(?<body>.*?)(?=^## |\z)')
if(-not $formalMatch.Success){Skip-Invocation "FORMAL_STATE_UNRESOLVED";return}
$activeMatch=[regex]::Match($formalMatch.Groups["body"].Value,'C(?<id>\d{3}) ACTIVE / (?<state>NOT YET JUDGED|INVALID ATTEMPT RECOVERY)')
if(-not $activeMatch.Success -or $activeMatch.Groups["id"].Value -ne "215"){Skip-Invocation "STALE_EXPERIMENT";return}
$runnerPath=Join-Path $Root "tools\run_c215.ps1";$runnerTokens=$null;$runnerParseErrors=$null
[System.Management.Automation.Language.Parser]::ParseFile($runnerPath,[ref]$runnerTokens,[ref]$runnerParseErrors)|Out-Null
if($runnerParseErrors.Count -gt 0){Skip-Invocation "RUNNER_PARSE_ERROR" (($runnerParseErrors|%{$_.Message}) -join " | ");return}
$runArgs=@{
 ExpectedHead=$ExpectedHead
 C214Summary=(Join-Path $Root "runs\c214-v5f-memory-capsule-closure-c243403ed49c4ed38d9d82cff1eef2a5\summary.json")
 C213Summary=(Join-Path $Root "runs\c213-v5f-memory-operation-contract-04a2bd0ef91b4a4998de8c1c1b6214df\summary.json")
 C212Summary=(Join-Path $Root "runs\c212-v5e-deciding-holdout-4660a8313d344cc7a7859cdd0afba186\summary.json")
 C211Summary=(Join-Path $Root "runs\c211-v5e-deciding-manifest-3d7891a0bb5b425db029bbf316728def\summary.json")
 C210Summary=(Join-Path $Root "runs\c210-v5e-baseline-development-ed5d0ad0a17d41b9a576fc41683005cd\summary.json")
 C209Summary=(Join-Path $Root "runs\c209-v5e-visible-only-projection-4136fdb65cb643ffab274a898153d92c\summary.json")
 C208Summary=(Join-Path $Root "runs\c208-v5e-candidate-input-compat-cc0e510e762840c98f3d7cbb2b194652\summary.json")
 C207Summary=(Join-Path $Root "runs\c207-v5e-nine-family-dev-manifest-3079dd47bce44ed990278c52b888bae7\summary.json")
 C206Summary=(Join-Path $Root "runs\c206-v5e-terminal-derived-ce39ead8d3db41c0b7cde3b11442f6b0\summary.json")
 C205Summary=(Join-Path $Root "runs\c205-v5e-phase0-batch-attribution-dfe8de2821934f1785f5ce925ca2d3c9\summary.json")
 C204Summary=(Join-Path $Root "runs\c204-v5e-live-v2-mixed-channel-91f31086978f4d2fa54dfe8abcf78200\summary.json")
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
try { & { Write-Output "=== C215 repository preflight ===";Write-Output "branch = $branchNow";Write-Output "execution_head = $headNow";.\tools\run_c215.ps1 @runArgs } *>&1 | Tee-Object -FilePath $log } catch {$failure=$_} finally {
 try {.\tools\publish_experiment_log.ps1 -ExperimentId C215 -LogPath $log -ExecutionHead $ExpectedHead} catch {if($failure){throw "C215 execution failed and log publication also failed"};throw}
}
if($failure){throw $failure}
