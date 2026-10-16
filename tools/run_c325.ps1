param(
    [Parameter(Mandatory=$true)][string]$ExpectedHead,
    [Parameter(Mandatory=$true)][string]$Folder
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
if ($PSVersionTable.PSEdition -ne 'Core' -or $PSVersionTable.PSVersion -lt [version]'7.3') {
    throw 'PowerShell 7.3 or newer is required'
}
$PSNativeCommandArgumentPassing = 'Standard'
$Python = Join-Path $Root '.venv-py31315\Scripts\python.exe'
$Script = Join-Path $Root 'tools\c325_execution.py'
$oldEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONIOENCODING = 'utf-8'
    & $Python -B -X faulthandler -u $Script --root $Root --folder $Folder --expected-head $ExpectedHead
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        throw "C325 execution failed; exit=$code. Preserve this attempt; no automatic retry."
    }
}
finally { $env:PYTHONIOENCODING = $oldEncoding }
