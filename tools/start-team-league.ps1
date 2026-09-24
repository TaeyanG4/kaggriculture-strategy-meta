param(
  [int]$LeaguePort = 8791,
  [int]$GatewayPort = 8792,
  [switch]$Restart,
  [switch]$Tunnel
)
# Starts the league server in always-on team mode and the login gateway in front of it.
# -Restart restarts a running league server gracefully: stop battles, restart, resume continuous battles.
# -Tunnel also starts a Cloudflare quick tunnel to the gateway; its address changes whenever the tunnel restarts.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv\Scripts\python.exe'
$pythonw = Join-Path $root '.venv\Scripts\pythonw.exe'
$leagueScript = Join-Path $root 'tools\public_league.py'
$gatewayScript = Join-Path $root 'tools\league_gateway.py'
$leagueUrl = "http://127.0.0.1:$LeaguePort"
$gatewayUrl = "http://127.0.0.1:$GatewayPort"

function Test-Up([string]$url) {
  try { Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 5 | Out-Null; return $true } catch { return $false }
}

function Wait-State([string]$url, [bool]$up, [int]$seconds) {
  $deadline = (Get-Date).AddSeconds($seconds)
  while ((Get-Date) -lt $deadline) {
    if ((Test-Up $url) -eq $up) { return $true }
    Start-Sleep -Milliseconds 500
  }
  return $false
}

function Get-LeagueServer {
  @(Get-CimInstance Win32_Process -Filter "Name='pythonw.exe' OR Name='python.exe'" |
    Where-Object { $_.CommandLine -match 'public_league\.py"?\s+serve\b' -and $_.CommandLine -match "--port\s+$LeaguePort\b" })
}

& $python $gatewayScript check | Out-Null
if ($LASTEXITCODE -ne 0) {
  throw 'No team accounts yet. Create one first: .venv\Scripts\python.exe tools\league_gateway.py user add <nickname> --role admin'
}

$resume = $false
$focusId = $null
$focusRemaining = 0
if (Test-Up "$leagueUrl/api/progress") {
  $servers = Get-LeagueServer
  $browserMode = @($servers | Where-Object { $_.CommandLine -match '--exit-with-browser' }).Count -gt 0
  if ($Restart) {
    $progress = Invoke-RestMethod "$leagueUrl/api/progress"
    $battle = $progress.battle
    $resume = ($battle.phase -eq 'running') -and (-not $battle.focus_agent_id)
    if ($battle.phase -eq 'running' -and $battle.focus_agent_id) {
      # Games completed in the unfinished batch are kept, so only the rest is resumed.
      $current = if ($progress.cycle) { [int]$progress.cycle.completed } else { 0 }
      $focusRemaining = [int]$battle.focus_target_games - [int]$battle.focus_completed_games - $current
      if ($focusRemaining % 2) { $focusRemaining++ }
      if ($focusRemaining -ge 2) { $focusId = $battle.focus_agent_id }
      Write-Host "Focus run on agent $($battle.focus_agent_id) will resume with $focusRemaining games after the restart."
    }
    if ($battle.phase -ne 'stopped') {
      if ($battle.phase -eq 'running') { Invoke-RestMethod -Method Post "$leagueUrl/api/battle/toggle" | Out-Null }
      $deadline = (Get-Date).AddSeconds(120)
      do {
        Start-Sleep -Seconds 2
        $phase = (Invoke-RestMethod "$leagueUrl/api/progress").battle.phase
      } while ($phase -ne 'stopped' -and (Get-Date) -lt $deadline)
      if ($phase -ne 'stopped') { throw 'Battles did not stop within 120 seconds; nothing was restarted.' }
    }
    $servers | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    if (-not (Wait-State "$leagueUrl/api/progress" $false 20)) { throw "Port $LeaguePort is still serving after stopping the league server." }
    Write-Host 'League server stopped for restart.'
  } elseif ($browserMode) {
    Write-Warning 'The league server runs in browser-exit mode and stops when the last local dashboard tab closes. Run again with -Restart for always-on team mode.'
  }
}

if (-not (Test-Up "$leagueUrl/api/progress")) {
  Start-Process -FilePath $pythonw -ArgumentList @("`"$leagueScript`"", 'serve', '--port', "$LeaguePort") -WorkingDirectory $root -WindowStyle Hidden
  if (-not (Wait-State "$leagueUrl/api/progress" $true 60)) { throw "League server did not start on port $LeaguePort." }
  Write-Host "League server started (always-on): $leagueUrl"
  if ($resume) {
    Invoke-RestMethod -Method Post "$leagueUrl/api/battle/toggle" | Out-Null
    Write-Host 'Continuous battles resumed.'
  } elseif ($focusId) {
    $body = @{ agent_id = [int]$focusId; games = $focusRemaining } | ConvertTo-Json -Compress
    Invoke-RestMethod -Method Post "$leagueUrl/api/focus" -ContentType 'application/json' -Body $body | Out-Null
    Write-Host "Focus run on agent $focusId resumed: $focusRemaining games."
  }
}

if (-not (Test-Up "$gatewayUrl/gateway/login")) {
  Start-Process -FilePath $pythonw -ArgumentList @("`"$gatewayScript`"", 'serve', '--port', "$GatewayPort", '--upstream', $leagueUrl) -WorkingDirectory $root -WindowStyle Hidden
  if (-not (Wait-State "$gatewayUrl/gateway/login" $true 30)) { throw "Team gateway did not start on port $GatewayPort." }
}
Write-Host "League server (this PC only): $leagueUrl"
Write-Host "Team gateway (connect the tunnel here): $gatewayUrl"

if ($Tunnel) {
  $cloudflared = Join-Path $root 'state\public_league\bin\cloudflared.exe'
  $urlFile = Join-Path $root 'state\public_league\team_url.txt'
  $log = Join-Path $root 'state\public_league\cloudflared.log'
  if (-not (Test-Path $cloudflared)) { throw "cloudflared not found: $cloudflared" }
  $running = @(Get-CimInstance Win32_Process -Filter "Name='cloudflared.exe'" |
    Where-Object { $_.CommandLine -match "--url\s+http://127\.0\.0\.1:$GatewayPort\b" })
  if ($running.Count -and (Test-Path $urlFile)) {
    $address = (Get-Content $urlFile -Raw).Trim()
  } else {
    $running | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Remove-Item $log, $urlFile -ErrorAction SilentlyContinue
    Start-Process -FilePath $cloudflared -WindowStyle Hidden -ArgumentList @(
      'tunnel', '--no-autoupdate', '--logfile', "`"$log`"", '--url', "http://127.0.0.1:$GatewayPort")
    $address = $null
    $deadline = (Get-Date).AddSeconds(60)
    while (-not $address -and (Get-Date) -lt $deadline) {
      Start-Sleep -Seconds 1
      if (Test-Path $log) {
        $found = Select-String -Path $log -Pattern 'https://(?!api\.)[a-z0-9-]+\.trycloudflare\.com' | Select-Object -First 1
        if ($found) { $address = $found.Matches[0].Value }
      }
    }
    if (-not $address) { throw "Quick tunnel did not report an address; see $log" }
    Set-Content -Path $urlFile -Value $address -Encoding ASCII
  }
  Write-Host "Team address (share with teammates; changes when the tunnel restarts): $address"
}
