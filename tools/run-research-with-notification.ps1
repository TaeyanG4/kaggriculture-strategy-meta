param(
    [Parameter(Mandatory=$true)][string]$StateDir,
    [Parameter(Mandatory=$true)][string]$Label,
    [Parameter(Mandatory=$true)][string]$ScriptPath,
    [Parameter(Mandatory=$true)][int]$Stage
)
$ErrorActionPreference='Stop'
$researchRoot=Split-Path -Parent $PSScriptRoot
$researchDir=(Resolve-Path -LiteralPath $StateDir).Path
if((Test-Path -LiteralPath (Join-Path $researchDir 'completion-ready.json')) -or
   (Test-Path -LiteralPath (Join-Path $researchDir 'execution-error.json'))){
    throw 'Existing terminal receipt: review or recover separately; do not relaunch.'
}
$researchExit=1
try {
    & (Join-Path $researchRoot '.venv/Scripts/python.exe') -u -X utf8 $ScriptPath --stage $Stage
    $researchExit=$LASTEXITCODE
} finally {
    # The Python runner owns the global lease and writes immutable result receipts.
    # This wrapper consumes no model tokens and displays the native notification.
    & (Join-Path $PSScriptRoot 'notify-research-completion.ps1') -StateDir $researchDir -Label $Label
}
exit $researchExit
