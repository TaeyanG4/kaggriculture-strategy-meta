"""Unchanged common transactional importer with the versioned capture reader."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools import import_validation_league as bulk
from tools.captured_validation_import_v2 import checked_capture
from tools.validation_import_session import ValidationSession
original_prepare=bulk.prepare
def load(path):
    return checked_capture(path) if (Path(path)/'captured-import.json').exists() else bulk.checked_campaign(path)
def prepare(db,campaigns,explicit=None,loader=None):
    return original_prepare(db,campaigns,explicit=explicit,loader=loader or load)
if __name__=='__main__':
    bulk.prepare=prepare
    try:
        with ValidationSession():bulk.main()
    except (bulk.ImportRejected,ValueError) as error:
        print(json.dumps(dict(status='not_imported',error=str(error))));raise SystemExit(2)
