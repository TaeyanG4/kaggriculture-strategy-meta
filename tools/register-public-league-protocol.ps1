$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$vbs = Join-Path $root 'public-league.vbs'
if (-not (Test-Path -LiteralPath $vbs)) { throw "Missing launcher: $vbs" }

$scheme = 'kaggriculture-league'
$key = "HKCU:\Software\Classes\$scheme"
$commandKey = Join-Path $key 'shell\open\command'
$wscript = Join-Path $env:WINDIR 'System32\wscript.exe'
$command = '"' + $wscript + '" "' + $vbs + '" --no-browser "%1"'

New-Item -Path $commandKey -Force | Out-Null
Set-Item -Path $key -Value 'URL:Kaggriculture Public League'
New-ItemProperty -Path $key -Name 'URL Protocol' -Value '' -PropertyType String -Force | Out-Null
Set-Item -Path $commandKey -Value $command
Write-Host "Registered: ${scheme}:// -> $vbs"
