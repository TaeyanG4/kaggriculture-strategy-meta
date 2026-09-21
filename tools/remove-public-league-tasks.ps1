$ErrorActionPreference = 'Stop'
foreach ($name in @('Kaggriculture Public League Collect', 'Kaggriculture Public League Refresh', 'Kaggriculture Public League Dashboard')) {
  if (Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false
    Write-Host "Removed: $name"
  }
}
$vbs = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup\Kaggriculture Public League Dashboard.vbs'
if (Test-Path -LiteralPath $vbs) {
  Remove-Item -LiteralPath $vbs
  Write-Host "Removed: $vbs"
}
$protocol = 'HKCU:\Software\Classes\kaggriculture-league'
if (Test-Path $protocol) {
  Remove-Item -LiteralPath $protocol -Recurse -Force
  Write-Host 'Removed: kaggriculture-league URL protocol'
}
