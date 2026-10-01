"""Download once; preserve transport failures and exclude unavailable replays.

Source, action, accounting, and replay-integrity audits remain the caller's
responsibility and are never caught or converted to download skips here.
"""
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def download_or_skip(episode, destination, receipt_dir):
    from src.kaggriculture_meta.pilot import REPLAY_URL
    destination=Path(destination);receipt_dir=Path(receipt_dir)
    destination.parent.mkdir(parents=True,exist_ok=True);receipt_dir.mkdir(parents=True,exist_ok=True)
    receipt_path=receipt_dir/f'{episode}-download.json'
    if receipt_path.exists():
        receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
        if receipt['status']=='SKIPPED_DOWNLOAD_ERROR':return None
        assert receipt['status']=='AVAILABLE' and Path(receipt['replay'])==destination and destination.exists()
        return destination
    temporary=destination.with_suffix(destination.suffix+'.download')
    receipt=dict(at=datetime.now(timezone.utc).isoformat(),episode=episode,replay=str(destination),
        raw_download=str(temporary),policy='state/continuation-20260929/owner-download-skip-20260930.json',
        retry=False,normal_tls_verification=True)
    try:
        if destination.exists():
            payload=destination.read_bytes();receipt['cached']=True
        else:
            if temporary.exists():
                receipt.update(status='SKIPPED_DOWNLOAD_ERROR',reason='Prior download attempt exists; no automatic retry or overwrite.')
                receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');return None
            result=subprocess.run([str(Path(os.environ.get('SystemRoot','C:/Windows'))/'System32/curl.exe'),
                '--location','--fail','--silent','--show-error','--connect-timeout','15','--max-time','60',
                '--output',str(temporary),REPLAY_URL.format(episode_id=episode)],capture_output=True,text=True,
                timeout=70,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            receipt.update(exit_code=result.returncode,stderr=result.stderr)
            if result.returncode:
                receipt.update(status='SKIPPED_DOWNLOAD_ERROR',reason='HTTP/TLS/transport failure; continue available evidence.')
                receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');return None
            payload=temporary.read_bytes()
        data=json.loads(payload)
        if not isinstance(data,dict) or not isinstance(data.get('steps'),list):
            receipt.update(status='SKIPPED_DOWNLOAD_ERROR',reason='Downloaded response is not a replay object.')
            receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');return None
    except (OSError,subprocess.TimeoutExpired,UnicodeDecodeError,json.JSONDecodeError) as error:
        receipt.update(status='SKIPPED_DOWNLOAD_ERROR',reason=type(error).__name__+': '+str(error))
        receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');return None
    if not destination.exists():temporary.replace(destination)
    receipt.update(status='AVAILABLE',bytes=len(payload),states=len(data['steps']))
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return destination
