param(
  # "tag=agent\file.py" pairs; defaults = the candidates ready now
  [string[]]$Candidates = @(
    "o159b=agent\o159b_feed_margin06.py",
    "o161=agent\o161_harvest_only.py",
    "o162=agent\o162_goose_only.py",
    "r000=agent\r000_terminal_hold.py",
    "c155=agent\c155_milk_externality.py"
  ),
  [switch]$SkipPool,
  [string]$Pool = "o_tools\pool_lean.json",
  [int]$Seeds = 8,
  [string]$ChunkDir = "o_replays\elite_chunks12",   # 12 chunks; c0..c5 layout kept for old results
  [int]$PoolWorkers = 12,
  [string]$SuiteDir = "elite_suite"   # results root under o_results; use with -ChunkDir for a holdout suite (elite2)
)
# Runs suite (6 chunk processes) + pool (1 process) per candidate in the background and polls result
# files, so one status line shows the current step AND the whole batch (elapsed / ETA) in real time.
$root = "H:\dev\kaggle-data\kaggriculture-strategy-meta"
$py = "$root\.venv\Scripts\python.exe"
$poolTag = [IO.Path]::GetFileNameWithoutExtension($Pool)
$poolN = @((Get-Content "$root\$Pool" -Raw -Encoding UTF8 | ConvertFrom-Json).PSObject.Properties).Count
$chunks = Get-ChildItem "$root\$ChunkDir" -Directory
$env:KAGG_VERIFY_CACHE = "$root\o_results\_verify_cache"   # skip re-verifying the original game per candidate
$suiteN = ($chunks | ForEach-Object { (Get-ChildItem $_.FullName -Filter '*-replay.json').Count } | Measure-Object -Sum).Sum
# time weights (seconds/unit, measured): suite ~2 s/episode with 6 chunks, pool ~2*Seeds s/opponent
$wSuite = 1.0; $wPool = 1.5 * $Seeds

function Bar($frac) { $n = [int][Math]::Round(20 * [Math]::Min(1, [Math]::Max(0, $frac))); ('#' * $n).PadRight(20, '.') }
function Fmt($sec) { if ($sec -lt 0) { return "--:--" }; "{0:hh\:mm\:ss}" -f [TimeSpan]::FromSeconds([int]$sec) }
function SuiteDone($tag) {  # finished episodes = results.json entries + in-progress log lines (logs are reset per run)
  $d = 0
  foreach ($c in $chunks) {
    $log = "$root\o_results\$SuiteDir\$tag.$($c.Name).log"
    if (Test-Path $log) { $d += @(Select-String -Path $log -Pattern '^\d+ episode=').Count }
  }
  $d
}
function SuiteSaved($tag) {
  $d = 0
  Get-ChildItem "$root\o_results\$SuiteDir\$tag\c*\results.json" -ErrorAction SilentlyContinue |
    ForEach-Object { $d += (Get-Content $_.FullName -Raw -Encoding UTF8 | ConvertFrom-Json).Count }  # UTF8: opponent names are non-ASCII
  $d
}
function PoolDone($dir) { if (Test-Path $dir) { @(Get-ChildItem $dir -Filter '*.json' | Where-Object { $_.Name -ne '_summary.json' }).Count } else { 0 } }

# build step list, skipping completed ones, so overall weights are exact
$steps = @()
foreach ($c in $Candidates) {
  $tag, $file = $c.Split("=", 2)
  if ((SuiteSaved $tag) -lt $suiteN) { $steps += [pscustomobject]@{ tag = $tag; file = $file; kind = 'suite'; total = $suiteN; w = $wSuite } }
  else { Write-Host "  $tag suite: already complete, skipping" }
  if (-not $SkipPool) {
    $poolDir = "$root\o_results\pool_${poolTag}_vs_$tag"
    if (Test-Path "$poolDir\_summary.json") { Write-Host "  $tag pool: already complete, skipping" }
    else { $steps += [pscustomobject]@{ tag = $tag; file = $file; kind = 'pool'; total = $poolN; w = $wPool; dir = $poolDir } }
  }
}
$totalW = ($steps | ForEach-Object { $_.w * $_.total } | Measure-Object -Sum).Sum
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$doneW = 0.0; $skipW = 0.0
Write-Host ("batch: {0} steps, est. total ~{1}" -f $steps.Count, (Fmt $totalW)) -ForegroundColor Cyan
New-Item -ItemType Directory -Force "$root\o_results\$SuiteDir" | Out-Null

for ($si = 0; $si -lt $steps.Count; $si++) {
  $s = $steps[$si]
  $procs = @()
  $pre = if ($s.kind -eq 'suite') { SuiteSaved $s.tag } else { PoolDone $s.dir }  # resumed work: excluded from rate estimates
  $skipW += $s.w * $pre
  if ($s.kind -eq 'suite') {
    foreach ($c in $chunks) {
      $k = $c.Name; $out = "$root\o_results\$SuiteDir\$($s.tag)\$k"
      $procs += Start-Process -FilePath $py -ArgumentList "-m", "src.kaggriculture_meta.replay_lab", "--candidate", "$root\$($s.file)", "--replays", $c.FullName, "--out", $out, "--mode", "fixed_shops_frozen_opponent" -WorkingDirectory $root -NoNewWindow -PassThru -RedirectStandardOutput "$root\o_results\$SuiteDir\$($s.tag).$k.log" -RedirectStandardError "$root\o_results\$SuiteDir\$($s.tag).$k.err"
    }
  }
  else {
    $procs += Start-Process -FilePath $py -ArgumentList "$root\tools\o_tournament.py", "--pool", "$root\$Pool", "--ref", "$root\$($s.file)", "--seeds", $Seeds, "--seed-base", 7000, "--workers", $PoolWorkers, "--out", $s.dir -WorkingDirectory $root -NoNewWindow -PassThru -RedirectStandardOutput "$($s.dir).log" -RedirectStandardError "$($s.dir).err"
  }
  $stepSw = [System.Diagnostics.Stopwatch]::StartNew()
  $lastLen = 0
  try {
  while ($true) {
    $d = if ($s.kind -eq 'suite') { SuiteDone $s.tag } else { PoolDone $s.dir }
    $d = [Math]::Min($d, $s.total)
    $alive = @($procs | Where-Object { -not $_.HasExited }).Count
    if ($alive -eq 0) { $d = $s.total }
    $stepFrac = $d / [Math]::Max(1, $s.total)
    $new = [Math]::Max(0, $d - $pre)
    $stepEta = if ($new -gt 0) { $stepSw.Elapsed.TotalSeconds / $new * ($s.total - $d) } else { $s.w * ($s.total - $d) }
    $curW = $doneW + $s.w * $d
    $allFrac = $curW / [Math]::Max(1, $totalW)
    # overall ETA: measured rate (this run's work only) once >5% done, else the prior weights
    $runW = $curW - $skipW
    $allEta = if ($allFrac -gt 0.05 -and $runW -gt 0) { $sw.Elapsed.TotalSeconds / $runW * ($totalW - $curW) } else { $totalW - $curW }
    $line = ("`r[{0}/{1} {2} {3}] [{4}] {5}/{6} eta {7} | ALL [{8}] {9,3}% elapsed {10} eta {11}" -f ($si + 1), $steps.Count, $s.tag, $s.kind, (Bar $stepFrac), $d, $s.total, (Fmt $stepEta), (Bar $allFrac), [int](100 * $allFrac), (Fmt $sw.Elapsed.TotalSeconds), (Fmt $allEta))
    Write-Host -NoNewline ($line.PadRight($lastLen)); $lastLen = $line.Length
    if ($alive -eq 0) { break }
    Start-Sleep -Seconds 5
  }
  }
  finally {  # Ctrl+C: stop the workers so a re-run resumes cleanly (results are per-episode / per-opponent)
    $procs | Where-Object { -not $_.HasExited } | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
  }
  Write-Host ""
  $doneW += $s.w * $s.total
  if ($s.kind -eq 'suite') {
    $errs = Get-ChildItem "$root\o_results\$SuiteDir" -Filter "$($s.tag).*.err" | Where-Object { $_.Length -gt 0 }
    if ($errs) { Write-Host "  stderr non-empty: $($errs.Name -join ', ')" -ForegroundColor Yellow }
  }
  else { Get-Content "$($s.dir).log" -Tail 1 }
}

Write-Output ("`n=== SUMMARY (elapsed {0}) ===" -f (Fmt $sw.Elapsed.TotalSeconds))   # Write-Output so Tee-Object files carry the completion marker
foreach ($c in $Candidates) {
  $tag, $file = $c.Split("=", 2)
  Write-Host "--- $tag : elite suite vs c150" -ForegroundColor Yellow
  & $py "$root\o_tools\suite_summary.py" $tag c150 $SuiteDir
  if (-not $SkipPool) {
    Write-Host "--- $tag : pool vs c150 (per-opponent delta; positive = better)" -ForegroundColor Yellow
    & $py "$root\o_tools\compare_pool_results.py" "$root\o_results\pool_${poolTag}_vs_c150" "$root\o_results\pool_${poolTag}_vs_$tag" | Select-Object -Last 12
  }
}
