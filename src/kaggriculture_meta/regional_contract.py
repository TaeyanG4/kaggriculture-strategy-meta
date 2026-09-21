"""Lossless region-service contracts; no optimization or policy decisions.

Input rows are explicit pre-action positions and commands.  A caller must label
whether these are forecasts or observed events; this module makes no guarantee
that a forecast is executable. Multiple actors and visits per tile are retained.
"""
from collections import defaultdict

MOVES = {'NORTH': (0, -1), 'SOUTH': (0, 1), 'EAST': (1, 0), 'WEST': (-1, 0)}
SERVICES = {'PLANT', 'WATER', 'FERTILIZE', 'HARVEST', 'DIG'}

def after_position(pos, command, board=10):
    x, y = pos
    if command[0] in MOVES:
        dx, dy = MOVES[command[0]]
        if 0 <= x+dx < board and 0 <= y+dy < board:
            x, y = x+dx, y+dy
    return [x, y]

def compile_day(events, region, board=10, replaceable=None):
    """Keep non-region service barriers fixed; store asynchronous task tokens."""
    region = set(map(tuple, region))
    groups = defaultdict(list)
    for e in events:
        groups[e['actor']].append(e)
    windows, barriers = [], []
    def close(rows, actor):
        if not rows:
            return
        start = rows[0]['step']; pos = list(rows[0]['pos']); tokens = []
        for e in rows:
            assert e['step'] == start + len(tokens)
            assert list(e['pos']) == pos
            command = list(e['action'])
            kind = 'move' if command[0] in MOVES else 'idle' if command[0]=='PASS' else 'service'
            tokens.append(dict(offset=e['step']-start, kind=kind, position=list(pos), command=command))
            pos = after_position(pos, command, board)
        windows.append(dict(actor=actor, start_step=start, end_step=rows[-1]['step'],
                            start=list(rows[0]['pos']), end=pos, tokens=tokens))
    for actor, rows in sorted(groups.items()):
        block = []
        for e in sorted(rows, key=lambda x:x['step']):
            if block and e['step'] != block[-1]['step']+1:
                close(block, actor); block=[]
            op=e['action'][0]
            permitted = (op in MOVES or op=='PASS' or tuple(e['pos']) in region and op in SERVICES)
            if replaceable is not None:
                permitted = permitted and replaceable(e)
            if permitted:
                block.append(e)
            else:
                close(block, actor);block=[]
                barriers.append(dict(step=e['step'],actor=actor,pos=list(e['pos']),action=list(e['action'])))
        close(block, actor)
    return dict(windows=windows,barriers=barriers,region=sorted(map(list,region)))

def compile_leases(events, region, board=10):
    """Prospective ownership boundaries; not a guarantee against all overlays.

    A native idle suffix from noon is owned by v9's existing courier. Subsequent
    PLANT on a target transfers that tile back to the parent's adaptive crop
    continuation. Such rows become fixed barriers, not planner reservations.
    No replay outcomes or opponent identity are used here.
    """
    region=set(map(tuple,region));last_nonpass={};crop_continuation={}
    for e in events:
        if e['action'][0]!='PASS':
            last_nonpass[e['actor']]=max(e['step'],last_nonpass.get(e['actor'],-1))
        if e['step']//24>11 and tuple(e['pos']) in region and e['action'][0]=='PLANT':
            p=tuple(e['pos']);crop_continuation[p]=min(e['step'],crop_continuation.get(p,10**9))
    def permitted(e):
        if e['action'][0]=='PASS' and e['step']%24>=12 and e['step']>last_nonpass.get(e['actor'],-1):
            return False
        if tuple(e['pos']) in crop_continuation and e['step']>=crop_continuation[tuple(e['pos'])] and e['action'][0] in SERVICES:
            return False
        return True
    result=compile_day(events,region,board,replaceable=permitted)
    result['limits']='Courier suffix and crop continuation excluded; actual execution/resource guard still required.'
    return result

def decode(contract):
    commands={}
    for w in contract['windows']:
        pos=list(w['start'])
        for token in w['tokens']:
            assert pos==token['position']
            key=(w['start_step']+token['offset'],w['actor'])
            assert key not in commands
            commands[key]=dict(pos=list(pos),action=list(token['command']))
            pos=after_position(pos,token['command'])
        assert pos==w['end']
    for b in contract['barriers']:
        key=(b['step'],b['actor']);assert key not in commands
        commands[key]=dict(pos=list(b['pos']),action=list(b['action']))
    return commands

def forecast_day(obs, action, tape, spawn):
    """Use current observation/action and known own tape only (c321 semantics)."""
    start=int(obs['step']);assert start%24==0
    farm=obs['farms'][int(obs['player'])];board=len(farm['tiles'])
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    events=[]
    for step in range(start,min(start+24,719)):
        a=action if step==start else tape(step)
        units=[a.get('farmer') or ['PASS']]+list(a.get('hands') or [])
        for actor,pos in enumerate(positions):
            cmd=list(units[actor] if actor<len(units) and units[actor] else ['PASS'])
            events.append(dict(step=step,actor=actor,pos=list(pos),action=cmd))
            positions[actor]=after_position(pos,cmd,board)
        for _ in range(sum(1 for o in a.get('market') or [] if o and o[0]=='HIRE')):
            positions.append(list(spawn(positions,board)))
    return events
