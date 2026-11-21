param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
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
$formal = [regex]::Match($handoff,'(?ms)^## Formal state\s+(?<body>.*?)(?=^## |\z)')
if (-not $formal.Success) { Skip-Invocation "FORMAL_STATE_UNRESOLVED"; return }
$active = [regex]::Matches($formal.Groups["body"].Value,'C(?<id>\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)')
if ($active.Count -ne 1 -or $active[0].Groups["id"].Value -ne "300") { Skip-Invocation "STALE_EXPERIMENT"; return }
$runnerPath = Join-Path $Root "tools\run_c300.ps1"
$runnerTokens = $null; $runnerErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($runnerPath,[ref]$runnerTokens,[ref]$runnerErrors) | Out-Null
if ($runnerErrors.Count -gt 0) { Skip-Invocation "RUNNER_PARSE_ERROR"; return }
$Summaries = @(
    (Join-Path $Root "runs\c299-v5b-core-grid-d118c6d85dfa47dbaac6ce40655b2fe6\summary.json"),
    (Join-Path $Root "runs\c298-v5b-components-13bf02bea0764e2cb8fe8802cfa52eb7\summary.json"),
    (Join-Path $Root "runs\c297-v5b-init-order-1e8b2002a1e142db81c0c8b5d51a1b4a\summary.json"),
    (Join-Path $Root "runs\c296-v5b-render-batches-653d5ee53ab747f69da1611a8fc69630\summary.json"),
    (Join-Path $Root "runs\c295-v5b-ce-budget-2361f7495977449a9c95d5dfff51d6ad\summary.json"),
    (Join-Path $Root "runs\c294-v5b-support-choice-79d31882e59f46fe933bb7e863bad8e2\summary.json"),
    (Join-Path $Root "runs\c293-v5b-fact-support-834c844c03c84023bc4ef1c6d32e3067\summary.json"),
    (Join-Path $Root "runs\c292-v5b-answer-roles-ba65b6ac20ac46e5b08fe96a5e5a8e74\summary.json"),
    (Join-Path $Root "runs\c291-v5b-answer-margin-7f15f2dbf9ca4a16a2ba0ce2271a3421\summary.json"),
    (Join-Path $Root "runs\c290-v5b-pair-margin-dd335cb112744775980aa441008b9a7f\summary.json"),
    (Join-Path $Root "runs\c289-v5b-early-pair-ac332442137243e68d4ec3bd754ba717\summary.json"),
    (Join-Path $Root "runs\c288-v5b-pair-assignment-f6a7427e94c44fc7b818f8cd18626562\summary.json"),
    (Join-Path $Root "runs\c287-v5b-fit-partition-fb83191e6dd74d3f840c59f9a5282069\summary.json"),
    (Join-Path $Root "runs\c286-v5b-cosine-tail-1664d75f4cf649fb8c5ca98f4be8308b\summary.json"),
    (Join-Path $Root "runs\c285-v5b-saved-length-audit-94786461780e4110a04f18ca3c92c427\summary.json"),
    (Join-Path $Root "runs\c284-v5b-max-length-450fab44535d4dd09c14931b8de1a283\summary.json"),
    (Join-Path $Root "runs\c283-v5b-frozen-four-bacee738e5a04007ae0f0f3093b0f5a7\summary.json"),
    (Join-Path $Root "runs\c282-v5b-mixed-length-5ad726e62dfa4eacada5a8cda8c4c27f\summary.json"),
    (Join-Path $Root "runs\c281-v5b-saved-support-audit-674eda46d9634e258004cabe55550065\summary.json"),
    (Join-Path $Root "runs\c280-v5b-evidence-only-dual-bb662d609be24ad9a1fd20d4aef54174\summary.json"),
    (Join-Path $Root "runs\c279-v5b-saved-dual-audit-e6d76ea781994de085b16ea8e7a6b972\summary.json"),
    (Join-Path $Root "runs\c278-v5b-mean-final-dual-c1d5206c6c6a48ab98acd15c5cb8aa71\summary.json"),
    (Join-Path $Root "runs\c277-v5b-saved-lr-audit-7e9cad9663144ae9bdbacda802c21306\summary.json"),
    (Join-Path $Root "runs\c276-v5b-final-boundary-lr-dcd7c7c2f13d49209c05bd4b2ca43110\summary.json"),
    (Join-Path $Root "runs\c275-v5b-gate-failure-audit-fb5be8dc32064545aa7a993b70e50706\summary.json"),
    (Join-Path $Root "runs\c274-v5b-directional-boundary-06a7a84bf4554f83b5cb6e099a828178\summary.json")
)
$runArgs = @{Summaries=$Summaries; ExpectedHead=$ExpectedHead}
New-Item -ItemType Directory -Path (Join-Path $Root "runs") -Force | Out-Null
$preflightLog = Join-Path $Root "runs\c300-preflight-last.log"
$log = Join-Path $Root "runs\chatgpt-last.log"
$preflightFailure = $null
try { & $runnerPath @runArgs -Mode Validate *>&1 | Tee-Object -FilePath $preflightLog }
catch { $preflightFailure = $_ }
if ($null -ne $preflightFailure) {
    Skip-Invocation "AUTHORING_RUNTIME_PREFLIGHT_FAILED" $preflightFailure.Exception.Message
    return
}
$failure = $null
try {
    & {
        Write-Output "=== C300 repository preflight attestation ==="
        Get-Content -LiteralPath $preflightLog -Encoding UTF8
        Write-Output "=== C300 frozen inference diagnostic execution ==="
        Write-Output "execution_head = $headNow"
        & $runnerPath @runArgs -Mode Execute
    } *>&1 | Tee-Object -FilePath $log
}
catch { $failure = $_ }
finally {
    try { .\tools\publish_experiment_log.ps1 -ExperimentId C300 -LogPath $log -ExecutionHead $ExpectedHead }
    catch {
        if ($null -ne $failure) { throw "C300 execution and publication failed: $($failure.Exception.Message); $($_.Exception.Message)" }
        throw
    }
}
if ($null -ne $failure) { throw $failure }
