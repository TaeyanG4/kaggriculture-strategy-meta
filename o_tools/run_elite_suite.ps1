param([string]$Candidate, [string]$Tag)
$root = "H:\kaggle\competitions\kaggriculture-strategy-meta"
New-Item -ItemType Directory -Force "$root\o_results\elite_suite" | Out-Null
$chunks = Get-ChildItem "$root\o_replays\elite_chunks" -Directory
$total = ($chunks | ForEach-Object { (Get-ChildItem $_.FullName -Filter '*-replay.json').Count } | Measure-Object -Sum).Sum
$procs = @()
foreach ($c in $chunks) {
  $k = $c.Name
  $out = "$root\o_results\elite_suite\$Tag\$k"
  $procs += Start-Process -FilePath "$root\.venv\Scripts\python.exe" -ArgumentList "-m","src.kaggriculture_meta.replay_lab","--candidate","$root\$Candidate","--replays",$c.FullName,"--out",$out,"--mode","fixed_shops_frozen_opponent" -WorkingDirectory $root -NoNewWindow -PassThru -RedirectStandardOutput "$root\o_results\elite_suite\$Tag.$k.log" -RedirectStandardError "$root\o_results\elite_suite\$Tag.$k.err"
}
$sw = [System.Diagnostics.Stopwatch]::StartNew()
while ($true) {
  $done = 0
  foreach ($c in $chunks) {
    $log = "$root\o_results\elite_suite\$Tag.$($c.Name).log"
    if (Test-Path $log) { $done += @(Select-String -Path $log -Pattern '^\d+ episode=').Count }
  }
  $el = $sw.Elapsed.TotalSeconds
  if ($done -gt 0) { $eta = [int]($el / $done * ($total - $done)) } else { $eta = -1 }
  $pct = [int](100 * $done / [Math]::Max(1, $total))
  $etaText = if ($eta -ge 0) { "{0:mm\:ss}" -f [TimeSpan]::FromSeconds($eta) } else { "--:--" }
  $bar = ('#' * [int]($pct / 4)).PadRight(25, '.')
  Write-Host -NoNewline ("`r[$Tag] [$bar] $done/$total ($pct%)  elapsed {0:mm\:ss}  eta $etaText   " -f $sw.Elapsed)
  $alive = @($procs | Where-Object { -not $_.HasExited }).Count
  if ($alive -eq 0) { break }
  Start-Sleep -Seconds 5
}
Write-Host ""
$errs = Get-ChildItem "$root\o_results\elite_suite" -Filter "$Tag.*.err" | Where-Object { $_.Length -gt 0 }
if ($errs) { Write-Host "stderr non-empty: $($errs.Name -join ', ')" -ForegroundColor Yellow }
Write-Host ("done $Tag in {0:mm\:ss}" -f $sw.Elapsed)
