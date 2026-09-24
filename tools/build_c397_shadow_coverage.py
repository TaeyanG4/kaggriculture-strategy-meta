"""Extend c396's exact public-policy hypothesis set, without changing its rule."""
import argparse,base64,hashlib,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='a0b64d765c54ceeafc872ef2a249e3e8492eb5f2206800d035dbaaef31d5c480'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);parser.add_argument('--disabled',action='store_true')
    parser.add_argument('--parent',type=Path,default=ROOT/'agent/c396_public_shadow.py')
    parser.add_argument('--parent-sha256',default=PARENT_SHA)
    parser.add_argument('--review-dir',type=Path,default=ROOT/'state/c396/v15-herd-review')
    parser.add_argument('--candidate-id',default='c397')
    parser.add_argument('--source-ids',default='252,255,264')
    args=parser.parse_args()
    assert args.candidate_id.startswith('c') and args.candidate_id[1:].isdigit()
    parent=args.parent.read_bytes();assert hashlib.sha256(parent).hexdigest()==args.parent_sha256
    directory=args.review_dir
    provenance=json.loads((directory/'provenance.json').read_text(encoding='utf8'))
    extra={}
    for item in provenance:
        agent=item['agent'];raw=Path(agent['source_path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==agent['source_sha256']
        assert set(json.loads(agent['artifact_files_json']))<=set(['main.py','LICENSE.txt','NOTICE.txt'])
        qa=json.loads((directory/f"agent{agent['id']}-diagnostic.json").read_text(encoding='utf8'))
        assert (qa['exact_actions'],qa['exact_private'],qa['exact_public'])==(719,719,718)
        extra[str(agent['id'])]=base64.b85encode(zlib.compress(raw,9)).decode()
    assert set(extra)==set(args.source_ids.split(','))
    overlay='''

# c397: public shadow coverage expansion. Taeyang/Codex 2026-09-23.
# Adds Harvey Zhang V15 Market Stack, Dmitrii Gluzdov Herd-Safe Sale Window,
# and statma's ca20 variant; all embedded original source notices are retained.
# Only the hypothesis set changes. Source IDs below are internal dictionary
# keys, never a runtime opponent identifier or an input from Kaggle.
# No policy selection by replay, seed, future observation or private opponent data.
_C397_ENABLED = __ENABLED__
_C397_ADDED_SOURCES = __SOURCES__
if _C397_ENABLED:
    _C396_SOURCES.update(_C397_ADDED_SOURCES)
c397_submission_agent = agent
'''.replace('__ENABLED__',str(not args.disabled)).replace('__SOURCES__',repr(extra))
    if args.candidate_id!='c397':
        overlay=overlay.replace('c397',args.candidate_id).replace('_C397','_'+args.candidate_id.upper())
        overlay=overlay.replace('Adds Harvey Zhang V15 Market Stack, Dmitrii Gluzdov Herd-Safe Sale Window,\n# and statma\'s ca20 variant; all embedded original source notices are retained.',
            'Adds reviewed public sources '+args.source_ids+'; all embedded original source notices are retained.')
    payload=parent.rstrip()+overlay.encode();compile(payload,str(args.out),'exec')
    assert not args.out.exists();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(payload)
    print(args.out,hashlib.sha256(payload).hexdigest(),len(payload))

if __name__=='__main__':main()
