"""Bounded AST-only source inspection; never dump packed agent/model literals."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path',type=Path)
    parser.add_argument('--function',action='append',default=[])
    parser.add_argument('--assign',action='append',default=[])
    parser.add_argument('--at-line',type=int)
    parser.add_argument('--prefix',default='',help='Filter function/class metadata by name prefix')
    parser.add_argument('--after-line',type=int,default=0,help='Filter metadata to definitions at or after this line')
    parser.add_argument('--max-chars',type=int,default=5500)
    args=parser.parse_args()
    limit=max(500,min(12000,args.max_chars))
    source=args.path.read_text(encoding='utf-8-sig');tree=ast.parse(source)
    nodes=[]
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name in args.function and node.lineno>=args.after_line:
            if args.at_line is None or node.lineno==args.at_line:nodes.append(node)
        elif isinstance(node,ast.ClassDef):
            for member in node.body:
                if isinstance(member,(ast.FunctionDef,ast.AsyncFunctionDef)) and f'{node.name}.{member.name}' in args.function:
                    if args.at_line is None or member.lineno==args.at_line:nodes.append(member)
        elif isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            if any(isinstance(t,ast.Name) and t.id in args.assign for t in targets):nodes.append(node)
    if not args.function and not args.assign:
        text=json.dumps([dict(name=n.name,line=n.lineno,end=n.end_lineno) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name.startswith(args.prefix) and n.lineno>=args.after_line],ensure_ascii=False)
        print(text if len(text)<=limit else json.dumps(dict(error='metadata exceeds budget; select --function or --assign',characters=len(text))))
        return
    output=[];used=0
    for node in nodes:
        segment=ast.get_source_segment(source,node) or ''
        literals=[n.value for n in ast.walk(node) if isinstance(n,ast.Constant) and isinstance(n.value,(str,bytes))]
        packed=any(len(v)>500 for v in literals)
        header=f'{args.path.name}:{node.lineno}-{node.end_lineno}'
        if packed or len(segment)+len(header)+used+2>limit:
            rendered=header+' '+json.dumps(dict(omitted=True,reason='large literal' if packed else 'output budget',characters=len(segment),sha256=hashlib.sha256(segment.encode()).hexdigest()),ensure_ascii=False)
        else:rendered=header+'\n'+segment
        if used+len(rendered)+2>limit:break
        output.append(rendered);used+=len(rendered)+2
    result='\n\n'.join(output) or 'No matching top-level AST node.'
    assert len(result)<=limit
    print(result)

if __name__=='__main__':main()
