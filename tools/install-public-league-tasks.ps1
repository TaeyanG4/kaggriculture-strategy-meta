param(
  [int]$EveryMinutes = 30,
  [int]$Workers = 12,
  [int]$MaxMatches = 240,
  [int]$Port = 8791
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$python = Join-Path $root '.venv\Scripts\pythonw.exe'
if (-not (Test-Path $python)) { throw "Missing project Python: $python" }
$launcher = Join-Path $root 'tools\public_league.py'
$refreshArgs = '"' + $launcher + '" collect'

$refreshAction = New-ScheduledTaskAction -Execute $python -Argument $refreshArgs -WorkingDirectory $root
$refreshTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
  -RepetitionInterval (New-TimeSpan -Minutes $EveryMinutes) `
  -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable `
  -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun `
  -ExecutionTimeLimit (New-TimeSpan -Hours 8)
if (Get-ScheduledTask -TaskName 'Kaggriculture Public League Refresh' -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName 'Kaggriculture Public League Refresh' -Confirm:$false
}
Register-ScheduledTask -TaskName 'Kaggriculture Public League Collect' -Action $refreshAction `
  -Trigger $refreshTrigger -Settings $settings -Description 'Collect public Kaggriculture notebooks without starting league matches.' -Force | Out-Null

if (Get-ScheduledTask -TaskName 'Kaggriculture Public League Dashboard' -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName 'Kaggriculture Public League Dashboard' -Confirm:$false
}
$oldVbs = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup\Kaggriculture Public League Dashboard.vbs'
if (Test-Path -LiteralPath $oldVbs) { Remove-Item -LiteralPath $oldVbs }

& (Join-Path $PSScriptRoot 'register-public-league-protocol.ps1') | Out-Null

Write-Host 'Installed:'
Write-Host '  Kaggriculture Public League Collect'
Write-Host 'Dashboard server is session-scoped. Double-click public-league.html or public-league.vbs.'
Write-Host ("Dashboard: http://127.0.0.1:{0}" -f $Port)
