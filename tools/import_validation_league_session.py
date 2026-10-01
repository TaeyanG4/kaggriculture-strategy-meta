"""Run the common importer's unchanged CLI with per-invocation provenance reuse."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.validation_import_session import ValidationSession
from tools import import_validation_league as bulk

if __name__=='__main__':
    try:
        with ValidationSession() as session:
            bulk.main()
            print(json.dumps(dict(unique_hashed_files=len(session.files),digest_reuses=session.digest_hits,
                validated_ancestor_campaigns=len(session.campaigns),ancestor_reuses=session.campaign_hits)),file=sys.stderr)
    except (bulk.ImportRejected,ValueError) as error:
        print(json.dumps(dict(status='not_imported',error=str(error))));raise SystemExit(2)
