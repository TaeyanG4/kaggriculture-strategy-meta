param(
    [Parameter(Mandatory=$true)][string]$Config,
    [Parameter(Mandatory=$true)][string]$Out,
    [ValidateSet('screen','confirm','final')][string]$Stage='screen',
    [ValidateSet('Prepare','Check','Run','Analyze')][string]$Action='Check'
)
$ErrorActionPreference='Stop'
$ProgressPreference='Continue'
$validationRoot=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$validationPython=Join-Path $validationRoot '.venv/Scripts/python.exe'
$validationScript=Join-Path $PSScriptRoot 'validation_v2.py'
$validationConfig=(Resolve-Path -LiteralPath $Config).Path
$validationOut=[IO.Path]::GetFullPath($Out)
$validationLock=$null
$validationSuccess=$false
$validationOldGuard=$env:KAGGRICULTURE_VALIDATION_GUARDED
try {
    if ($Action -eq 'Run') {
        $validationLock=[IO.File]::Open((Join-Path $validationRoot 'state/agent_experiments/.kaggriculture-global-launch.lock'),'OpenOrCreate','ReadWrite','None')
        $validationProcesses=@(Get-CimInstance Win32_Process)
        $validationActive=@($validationProcesses | Where-Object {
            $_.Name -match '^python(w)?\.exe$' -and (
                $_.CommandLine -match 'kaggriculture_meta\.(?:replay_lab|championship_league|league|championship_phase1|benchmark)' -or
                $_.CommandLine -match 'validation_v[12]\.py\s+(?:run|worker)' -or
                (([string]$_.CommandLine).Replace('/','\').Contains($validationRoot+'\state\agent_experiments\')) -or
                (([string]$_.CommandLine).Replace('/','\').Contains($validationRoot+'\o_tools\')))
        })
        if ($validationActive.Count) { throw ('Other campaign/process active: '+($validationActive.ProcessId -join ', ')) }
    }
    # All entry paths re-check the supplied config against a frozen manifest.
    & $validationPython -X utf8 $validationScript prepare --config $validationConfig --stage $Stage --out $validationOut
    if ($LASTEXITCODE -ne 0) { throw 'Preparation/configuration check failed' }
    if ($Action -eq 'Prepare' -or $Action -eq 'Check') {
        $validationSuccess=$true
    } else {
        $validationLog=Join-Path $validationOut ('console-'+(Get-Date -Format 'yyyyMMdd-HHmmss-fff')+'.log')
        $validationErr=$validationLog+'.stderr'
        $env:KAGGRICULTURE_VALIDATION_GUARDED='1'
        $ErrorActionPreference='Continue'
        & $validationPython -u -X utf8 $validationScript $Action.ToLowerInvariant() --out $validationOut 2> $validationErr | ForEach-Object {
            $validationLine=[string]$_
            Add-Content -LiteralPath $validationLog -Value $validationLine -Encoding utf8
            if ($validationLine.StartsWith('PROGRESS|')) {
                $v=$validationLine.Substring(9) | ConvertFrom-Json
                $elapsed=[TimeSpan]::FromSeconds($v.elapsed).ToString('hh\:mm\:ss')
                $eta=if ($null -eq $v.eta) {'estimating'} else {[TimeSpan]::FromSeconds($v.eta).ToString('hh\:mm\:ss')}
                $status='{0}/{1} ({2:N1}%) | cached {3} | failed {4} | elapsed {5} | {6:N2}/s | ETA {7}' -f $v.done,$v.total,$v.percent,$v.cached,$v.failed,$elapsed,$v.rate,$eta
                Write-Progress -Id 701 -Activity "Kaggriculture $Stage" -Status $status -PercentComplete $v.percent
            } else { Write-Host $validationLine }
        }
        $validationExit=$LASTEXITCODE
        $ErrorActionPreference='Stop'
        if ($validationExit -ne 0) { Get-Content -LiteralPath $validationErr -Tail 20; throw 'Validation failed; inspect logs' }
        $validationResult=Get-Content -LiteralPath (Join-Path $validationOut 'results.json') -Raw | ConvertFrom-Json
        $validationManifest=Get-Content -LiteralPath (Join-Path $validationOut 'manifest.json') -Raw | ConvertFrom-Json
        if ($validationResult.status -ne 'complete' -or $validationResult.completed_jobs -ne $validationManifest.expected_jobs -or $validationResult.contract_sha256 -ne $validationManifest.contract_sha256) { throw 'Incomplete result contract' }
        $validationSuccess=$true
    }
} finally {
    $env:KAGGRICULTURE_VALIDATION_GUARDED=$validationOldGuard
    if ($null -ne $validationLock) { $validationLock.Dispose() }
    Write-Progress -Id 701 -Activity 'Kaggriculture validation' -Completed
    if ($Action -eq 'Run') {
        try {
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            $validationNotice=New-Object System.Windows.Forms.NotifyIcon
            $validationNotice.Icon=if ($validationSuccess) {[System.Drawing.SystemIcons]::Information} else {[System.Drawing.SystemIcons]::Warning}
            $validationNotice.Visible=$true
            $validationNotice.BalloonTipTitle='Kaggriculture validation'
            $validationNotice.BalloonTipText=if ($validationSuccess) {'Execution complete. Review results for performance.'} else {'Failed or interrupted. Results preserved; check logs.'}
            $validationNotice.ShowBalloonTip(10000)
            if ($validationSuccess) {[System.Media.SystemSounds]::Asterisk.Play()} else {[System.Media.SystemSounds]::Exclamation.Play()}
            Start-Sleep -Seconds 3
            $validationNotice.Dispose()
        } catch { try {[Console]::Beep(1000,500)} catch {} }
    }
}
