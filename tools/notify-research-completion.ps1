param(
    [Parameter(Mandatory=$true)][string]$StateDir,
    [Parameter(Mandatory=$true)][string]$Label,
    [int]$OwnerPid=0,
    [string]$CompletionFile='completion-ready.json',
    [string]$ErrorFile='execution-error.json'
)
$ErrorActionPreference='Stop'
$noticeDir=(Resolve-Path -LiteralPath $StateDir).Path
# The latest explicit owner preference supersedes the preserved older receipt.
function Test-NoticeEnabled {
    $noticeRoot=Split-Path -Parent $PSScriptRoot
    $currentPolicy=Join-Path $noticeRoot 'state/continuation-20260929/owner-request.json'
    if(Test-Path -LiteralPath $currentPolicy){
        $currentPreference=Get-Content -LiteralPath $currentPolicy -Raw -Encoding UTF8 | ConvertFrom-Json
        if($null -ne $currentPreference.windows_completion_notification){return [bool]$currentPreference.windows_completion_notification}
    }
    $oldPolicy=Join-Path $noticeRoot 'state/continuation-20260929/execution-mode-owner-update.json'
    if(Test-Path -LiteralPath $oldPolicy){
        $oldPreference=Get-Content -LiteralPath $oldPolicy -Raw -Encoding UTF8 | ConvertFrom-Json
        if($oldPreference.notification_mode -eq 'silent'){return $false}
    }
    return $true
}
if(-not (Test-NoticeEnabled)){return}
$noticeReceipt=Join-Path $noticeDir 'windows-notification.json'
$noticeProcessFile=Join-Path $noticeDir 'windows-notifier-process.json'
$noticeLock=$null
$noticeIcon=$null
function Save-Notice($Path,$Value) {
    $noticeJson=$Value | ConvertTo-Json -Depth 6
    [IO.File]::WriteAllText($Path+'.tmp',$noticeJson,(New-Object Text.UTF8Encoding($false)))
    Move-Item -LiteralPath ($Path+'.tmp') -Destination $Path -Force
}
try {
    # One notification owner per result directory; never run another campaign.
    $noticeLock=[IO.File]::Open((Join-Path $noticeDir '.windows-notification.lock'),'OpenOrCreate','ReadWrite','None')
    if (Test-Path -LiteralPath $noticeReceipt) {
        $noticePrevious=Get-Content -LiteralPath $noticeReceipt -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($noticePrevious.status -in @('requested','shown')) { return }
    }
    Save-Notice $noticeProcessFile @{pid=$PID;owner_pid=$OwnerPid;label=$Label;started=[DateTime]::UtcNow.ToString('o');mechanism='OS process-exit wait; no model calls'}
    $noticeDone=Join-Path $noticeDir $CompletionFile
    $noticeError=Join-Path $noticeDir $ErrorFile
    if (-not (Test-Path -LiteralPath $noticeDone) -and -not (Test-Path -LiteralPath $noticeError) -and $OwnerPid -gt 0) {
        $noticeOwner=Get-Process -Id $OwnerPid -ErrorAction SilentlyContinue
        if ($null -ne $noticeOwner) {
            $noticeOwner.WaitForExit()
        }
    }
    if(-not (Test-NoticeEnabled)){return}
    $noticeCompleted=Test-Path -LiteralPath $noticeDone
    if (-not $noticeCompleted -and -not (Test-Path -LiteralPath $noticeError) -and $OwnerPid -le 0) { return }
    $noticeTitle=if ($noticeCompleted) {"$Label 검증 완료"} else {"$Label 검증 확인 필요"}
    $noticeBody=if ($noticeCompleted) {'검수 실행과 후처리가 끝났습니다. Codex가 다음 10분 자동 확인에서 결과를 검토하고 작업을 이어갑니다.'} else {'검수가 오류 또는 중단으로 끝났습니다. 저장 결과를 보존했습니다. Codex가 다음 자동 확인에서 원인을 검토합니다.'}
    # Reuse the native NotifyIcon mechanism used by run-validation-v1/v2/v3.
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $noticeIcon=New-Object System.Windows.Forms.NotifyIcon
    $noticeIcon.Icon=if ($noticeCompleted) {[Drawing.SystemIcons]::Information} else {[Drawing.SystemIcons]::Warning}
    $noticeIcon.Text='Kaggriculture'
    $noticeIcon.BalloonTipTitle=$noticeTitle
    $noticeIcon.BalloonTipText=$noticeBody
    $noticeIcon.BalloonTipIcon=if ($noticeCompleted) {[Windows.Forms.ToolTipIcon]::Info} else {[Windows.Forms.ToolTipIcon]::Warning}
    $script:noticeShown=$false
    $noticeIcon.add_BalloonTipShown({$script:noticeShown=$true})
    $noticeIcon.Visible=$true
    $noticeRecord=@{at=[DateTime]::UtcNow.ToString('o');status='requested';label=$Label;completed=$noticeCompleted;title=$noticeTitle;body=$noticeBody;pid=$PID;mechanism='Windows Forms NotifyIcon';source=$(if($noticeCompleted){$noticeDone}else{$noticeError});model_calls=0}
    $noticeIcon.ShowBalloonTip(15000)
    Save-Notice $noticeReceipt $noticeRecord
    if ($noticeCompleted) {[Media.SystemSounds]::Asterisk.Play()} else {[Media.SystemSounds]::Exclamation.Play()}
    $noticeTimer=[Diagnostics.Stopwatch]::StartNew()
    while ($noticeTimer.Elapsed.TotalSeconds -lt 18) {
        [Windows.Forms.Application]::DoEvents()
        if ($script:noticeShown -and $noticeRecord.status -ne 'shown') {
            $noticeRecord.status='shown';$noticeRecord.shown_at=[DateTime]::UtcNow.ToString('o');Save-Notice $noticeReceipt $noticeRecord
        }
        Start-Sleep -Milliseconds 100
    }
} catch {
    Save-Notice (Join-Path $noticeDir 'windows-notification-error.json') @{at=[DateTime]::UtcNow.ToString('o');error=$_.Exception.Message;pid=$PID}
    throw
} finally {
    if ($null -ne $noticeIcon) {$noticeIcon.Dispose()}
    if ($null -ne $noticeLock) {$noticeLock.Dispose()}
}
