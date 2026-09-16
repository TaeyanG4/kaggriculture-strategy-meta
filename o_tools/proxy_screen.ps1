# Screen candidates against the planner proxy on pinned worlds: prints each candidate's own cash (A mean) and the proxy's cash.
# Usage: powershell -File o_tools/proxy_screen.ps1 -Cands agent/o227_stealth_drop.py,agent/o231_fert_tours.py [-Seeds 7000-7007]
param([string[]]$Cands = @('agent/o227_stealth_drop.py'), [string]$Seeds = '7000-7007', [string]$Out = 'o_results/proxy/screen.txt')
$env:PYTHONIOENCODING = 'utf-8'
foreach ($c in $Cands) {
  $tag = [IO.Path]::GetFileNameWithoutExtension($c)
  $line = & .venv/Scripts/python.exe o_tools/proxy_eval.py --a $c --b agent/opp_planner_proxy.py --seeds $Seeds --label "screen_$tag" 2>$null | Select-String '^\['
  "$(Get-Date -Format 'MM-dd HH:mm') $line" | Tee-Object -FilePath $Out -Append
}
