param(
  [Parameter(Mandatory=$true)][string]$Tag,
  [Parameter(Mandatory=$true)][string]$File,      # agent\xxx.py
  [string]$Base = "o199c",                          # comparison baseline tag
  [switch]$Full                                     # skip the early-reject gate
)
# Lean validation: suite (88) -> gate -> fast pool (10 opps x 8 seeds x 2 seats) -> holdout (40).
# ~5 min per candidate instead of ~12. Bank / 32-seed pool stay manual (finalists only).
$root = "H:\dev\kaggle-data\kaggriculture-strategy-meta"; $py = "$root\.venv\Scripts\python.exe"; $env:MPLBACKEND = "Agg"
$sw = [System.Diagnostics.Stopwatch]::StartNew()
& "$root\o_tools\run_batch.ps1" -SkipPool -Candidates @("$Tag=$File") | Out-Null
$s = & $py "$root\o_tools\suite_summary.py" $Tag $Base | Select-Object -Index 2,3
Write-Host ("[{0}] suite vs {1}: {2}" -f $Tag, $Base, ($s -join ' | ')) -ForegroundColor Cyan
$hi = [double](($s[1] -replace '.*CI \[[^,]*, *([-+0-9]+)\].*', '$1'))
$lo = [double](($s[1] -replace '.*CI \[ *([-+0-9]+),.*', '$1'))
if (-not $Full -and $hi -lt 50) { Write-Host ("[{0}] REJECT at suite gate (CI upper {1} < +50) in {2:mm\:ss}" -f $Tag, $hi, $sw.Elapsed) -ForegroundColor Red; return }
& "$root\o_tools\run_batch.ps1" -Pool "o_tools\pool_fast.json" -Candidates @("$Tag=$File") | Out-Null
& "$root\o_tools\run_batch.ps1" -SkipPool -ChunkDir "o_replays\elite2_chunks" -SuiteDir "elite2_suite" -Candidates @("$Tag=$File") | Out-Null
$p = & $py "$root\o_tools\compare_pool_results.py" "$root\o_results\pool_pool_fast_vs_$Base" "$root\o_results\pool_pool_fast_vs_$Tag" | Select-String "^mean delta|notably WORSE"
$h = & $py "$root\o_tools\suite_summary.py" $Tag $Base elite2_suite | Select-Object -Index 2,3
Write-Host ("[{0}] pool10 vs {1}: {2}" -f $Tag, $Base, (($p | ForEach-Object { $_.Line }) -join ' | ')) -ForegroundColor Cyan
Write-Host ("[{0}] holdout vs {1}: {2}" -f $Tag, $Base, ($h -join ' | ')) -ForegroundColor Cyan
$verdict = if ($lo -gt 0) { "KEEP-suite" } elseif ($hi -gt 0) { "n.s. (pool/holdout decide)" } else { "REJECT" }
Write-Host ("[{0}] verdict: {1}  ({2:mm\:ss})" -f $Tag, $verdict, $sw.Elapsed) -ForegroundColor Green
