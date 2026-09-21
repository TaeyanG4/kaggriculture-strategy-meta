param(
  [Parameter(Mandatory=$true)][int]$EveryMinutes,
  [Parameter(Mandatory=$true)][int]$Workers,
  [int]$MaxMatches = 240,
  [ValidateSet('Enabled','Disabled')]
  [string]$State = 'Enabled'
)
$ErrorActionPreference = 'Stop'
if ($EveryMinutes -lt 15 -or $EveryMinutes -gt 10080) { throw 'EveryMinutes must be 15..10080.' }
if ($Workers -lt 1 -or $Workers -gt 12) { throw 'Workers must be 1..12.' }
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$pythonw = Join-Path $root '.venv\Scripts\pythonw.exe'
$launcher = Join-Path $root 'tools\public_league.py'
if (-not (Test-Path $pythonw)) { throw "Missing project Python: $pythonw" }
$args = '"' + $launcher + '" collect'
$action = New-ScheduledTaskAction -Execute $pythonw -Argument $args -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
  -RepetitionInterval (New-TimeSpan -Minutes $EveryMinutes) `
  -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable `
  -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun `
  -ExecutionTimeLimit (New-TimeSpan -Hours 8)
if (Get-ScheduledTask -TaskName 'Kaggriculture Public League Refresh' -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName 'Kaggriculture Public League Refresh' -Confirm:$false
}
Register-ScheduledTask -TaskName 'Kaggriculture Public League Collect' -Action $action `
  -Trigger $trigger -Settings $settings -Description 'Collect public Kaggriculture notebooks without starting league matches.' -Force | Out-Null
if ($State -eq 'Disabled') {
  Disable-ScheduledTask -TaskName 'Kaggriculture Public League Collect' | Out-Null
}
