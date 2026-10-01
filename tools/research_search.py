"""Find evidence paths without printing packed sources or replay contents."""
import argparse
import subprocess

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pattern')
    p.add_argument('paths', nargs='+')
    p.add_argument('--glob', action='append', default=[])
    p.add_argument('--limit', type=int, default=30)
    args=p.parse_args()
    cmd=['rg','--files-with-matches','--max-columns','220','--max-filesize','2M']
    for glob in args.glob:cmd.extend(['--glob',glob])
    cmd.extend(['--',args.pattern,*args.paths])
    result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode not in (0,1):
        raise SystemExit(result.stderr[:1200])
    paths=result.stdout.splitlines()
    print('\n'.join(paths[:args.limit]))
    if len(paths)>args.limit:print(f'({len(paths)-args.limit} more paths; narrow the pattern or scope)')

if __name__=='__main__':main()
