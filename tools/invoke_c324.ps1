param([Parameter(Mandatory=$true)][string]$ExpectedHead)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
function Skip-Invocation {
    param([string]$Reason,[string]$Detail='')
    Write-Output "invocation_skipped = $Reason"
    if ($Detail) { Write-Output "detail = $Detail" }
    Write-Output 'experiment_executed = False'
    Write-Output 'execution_log_publish_attempted = False'
}
if ($PSVersionTable.PSEdition -ne 'Core' -or $PSVersionTable.PSVersion -lt [version]'7.3') { Skip-Invocation 'POWERSHELL_7_3_REQUIRED'; return }
$PSNativeCommandArgumentPassing = 'Standard'
$branch = git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branch -ne 'feat/sft-target-loss') { Skip-Invocation 'WRONG_BRANCH'; return }
$dirty = @(git status --porcelain --untracked-files=no)
if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { Skip-Invocation 'DIRTY_TRACKED_TREE'; return }
$headNow = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $headNow -ne $ExpectedHead) { Skip-Invocation 'STALE_EXPECTED_HEAD'; return }
$handoff = Get-Content -LiteralPath (Join-Path $Root 'docs\experiment-ledger-and-handoff.md') -Raw -Encoding UTF8
$formal = [regex]::Match($handoff,'(?ms)^## Formal state\s+(?<body>.*?)(?=^## |\z)')
$active = [regex]::Matches($formal.Groups['body'].Value,'C(?<id>\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)')
if (-not $formal.Success -or $active.Count -ne 1 -or $active[0].Groups['id'].Value -ne '324') { Skip-Invocation 'STALE_EXPERIMENT'; return }
# Invalid native execution routes to bounded recovery diagnostics, never to another full run.
if ($active[0].Value -match 'INVALID ATTEMPT RECOVERY') {
    $actions = @{
        NATIVE_DIAGNOSTIC_R2 = 'tools\invoke_c324_native_diagnostic_r2.ps1'
        PARENT_PROFILE_R3 = 'tools\invoke_c324_parent_profile_r3.ps1'
        LOCKED_HASH_R4 = 'tools\invoke_c324_locked_hash_r4.ps1'
        VERIFIED_SESSION_R5 = 'tools\invoke_c324_verified_session_r5.ps1'
    }
    $selected = [regex]::Matches($formal.Groups['body'].Value,'(?m)^recovery_action = (?<action>[A-Z0-9_]+)\s*$')
    if ($selected.Count -ne 1 -or -not $actions.ContainsKey($selected[0].Groups['action'].Value)) { Skip-Invocation 'RECOVERY_ACTION_UNREGISTERED'; return }
    $recovery = Join-Path $Root $actions[$selected[0].Groups['action'].Value]
    $recoveryTokens = $null; $recoveryErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($recovery,[ref]$recoveryTokens,[ref]$recoveryErrors) | Out-Null
    if ($recoveryErrors.Count -gt 0) { Skip-Invocation 'RECOVERY_PARSE_ERROR'; return }
    & $recovery -ExpectedHead $ExpectedHead
    return
}
$runner = Join-Path $Root 'tools\run_c324.ps1'
$tokens = $null; $errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($runner,[ref]$tokens,[ref]$errors) | Out-Null
if ($errors.Count -gt 0) { Skip-Invocation 'RUNNER_PARSE_ERROR'; return }
$Summaries = @(
    (Join-Path $Root "runs\c323-v5b-fact-order-f1b710e74fbe495aba6410d0d9530248\summary.json"),
    (Join-Path $Root "runs\c322-v5b-query-contrast-f164844010f04c24bcfda4a743b44a72\summary.json"),
    (Join-Path $Root "runs\c321-v5b-interior-order-ef98962d405b402ba3926a6d1c2625b2\summary.json"),
    (Join-Path $Root "runs\c320-v5b-unequal-names-d1599525908a404998a52011a5567b81\summary.json"),
    (Join-Path $Root "runs\c319-v5b-trained-last-0f94e96bbbba43b395fcf8eab1e38246\summary.json"),
    (Join-Path $Root "runs\c318-v5b-readout-branches-bb278106ee824f26996434d7d895726a\summary.json"),
    (Join-Path $Root "runs\c317-v5b-query-endpoint-88ae97edc7d44cd3bcd9732e66c8b14e\summary.json"),
    (Join-Path $Root "runs\c316-v5b-single-replication-633dc1183add481189698a356817d951\summary.json"),
    (Join-Path $Root "runs\c315-v5b-single-mix-dbdffe0b88094f729d1dbfbcdba520f0\summary.json"),
    (Join-Path $Root "runs\c314-v5b-six-boundary-31c4ca923fa8459cbe9afde6fade9c83\summary.json"),
    (Join-Path $Root "runs\c313-v5b-frozen-six-8ef41237b7f84f148a0dcdce4b9aed21\summary.json"),
    (Join-Path $Root "runs\c312-v5b-value-batches-c23759c73f5c4bfbb03a7c3d9c8e8198\summary.json"),
    (Join-Path $Root "runs\c311-v5b-error-context-2e3d082f8a9a4045b09dbe38a62ca6a8\summary.json"),
    (Join-Path $Root "runs\c310-v5b-value-renaming-580abae854514a7fb49fe1f702f4b50d\summary.json"),
    (Join-Path $Root "runs\c309-v5b-core-lr-replication-e24b3b724e47415eae204d3084a68185\summary.json"),
    (Join-Path $Root "runs\c308-v5b-core-lr-02b24ac7b9da4a36a14a5545bd42aab6\summary.json"),
    (Join-Path $Root "runs\c307-v5b-core-replication-468c370e9c4b491585226c5492a8b52c\summary.json"),
    (Join-Path $Root "runs\c306-v5b-broad-core-freeze-f8b13e726f314db09555a293f6d6bdf8\summary.json"),
    (Join-Path $Root "runs\c305-v5b-length-overlap-4d5851c168fc401cbc5926f1d1ca841c\summary.json"),
    (Join-Path $Root "runs\c304-v5b-length-breadth-5090e7ce18a8444e9095afe14ad41266\summary.json"),
    (Join-Path $Root "runs\c303-v5b-gradient-route-ef832a6117c44389aa035cd16c76be70\summary.json"),
    (Join-Path $Root "runs\c302-v5b-gain-cross-d81285be58684cbfbb6d3ec7253a42ca\summary.json"),
    (Join-Path $Root "runs\c301-v5b-residual-gain-8e72f4cf3e744128b905da20770c9f5b\summary.json"),
    (Join-Path $Root "runs\c300-v5b-readout-terms-ba7889d232f342d591bb8b75f48cb853\summary.json"),
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
New-Item -ItemType Directory -Path (Join-Path $Root 'runs') -Force | Out-Null
$preflightLog = Join-Path $Root 'runs\c324-preflight-last.log'
$log = Join-Path $Root 'runs\chatgpt-last.log'
if (Test-Path -LiteralPath $preflightLog -PathType Leaf) {
    Copy-Item -LiteralPath $preflightLog -Destination (Join-Path $Root ('runs\c324-preflight-previous-' + [guid]::NewGuid().ToString('N') + '.log')) -ErrorAction Stop
}
try { & $runner @runArgs -Mode Validate *>&1 | Tee-Object -FilePath $preflightLog }
catch { Skip-Invocation 'AUTHORING_RUNTIME_PREFLIGHT_FAILED' $_.Exception.Message; return }
$failure = $null
try {
    & {
        Get-Content -LiteralPath $preflightLog -Encoding UTF8
        Write-Output "execution_head = $ExpectedHead"
        & $runner @runArgs -Mode Execute
    } *>&1 | Tee-Object -FilePath $log
}
catch { $failure = $_ }
finally {
    try { .\tools\publish_experiment_log.ps1 -ExperimentId C324 -LogPath $log -ExecutionHead $ExpectedHead }
    catch {
        if ($null -ne $failure) { throw "C324 execution and publication failed: $($failure.Exception.Message); $($_.Exception.Message)" }
        throw
    }
}
if ($null -ne $failure) { throw $failure }
