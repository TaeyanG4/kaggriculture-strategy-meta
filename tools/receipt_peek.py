"""Bounded JSON inspection: dotted paths, scalars, and collection metadata."""
import argparse
import json
from pathlib import Path

def compact(value,limit=240):
    if isinstance(value,dict):
        return {k:(compact(v,limit) if not isinstance(v,(dict,list)) else {'type':type(v).__name__,'length':len(v)}) for k,v in value.items()}
    if isinstance(value,list):
        return {'type':'list','length':len(value),'first_keys':list(value[0]) if value and isinstance(value[0],dict) else None}
    if isinstance(value,str) and len(value)>limit:return value[:limit]+'…'
    return value

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',type=Path);p.add_argument('keys',nargs='*')
    p.add_argument('--max-chars',type=int,default=3500)
    args=p.parse_args();obj=json.loads(args.file.read_text(encoding='utf-8-sig'))
    output={}
    for key in args.keys:
        value=obj
        for component in key.split('.'):
            value=value[int(component)] if isinstance(value,list) else value[component]
        output[key]=compact(value)
    if not args.keys:output=compact(obj)
    text=json.dumps(output,ensure_ascii=False,indent=2)
    if len(text)>args.max_chars:
        text=json.dumps({'file':str(args.file),'characters':len(text),'keys':list(output),'request':'Select fewer dotted keys.'},ensure_ascii=False)
    print(text)

if __name__=='__main__':main()
