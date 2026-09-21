param(
  [Parameter(Mandatory=$true)]
  [ValidateSet('Enabled','Disabled')]
  [string]$State
)
$ErrorActionPreference = 'Stop'
$name = 'Kaggriculture Public League Collect'
if (-not (Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue)) {
  throw "Scheduled task is not installed: $name"
}
if ($State -eq 'Enabled') {
  Enable-ScheduledTask -TaskName $name | Out-Null
} else {
  Disable-ScheduledTask -TaskName $name | Out-Null
}
