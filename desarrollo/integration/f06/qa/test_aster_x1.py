"""T01–T15 native QA contract. Tick tests do not certify real MSI latency."""
import argparse
import json
from pathlib import Path
import subprocess
import time


def run(runner, output):
    output.mkdir(parents=True, exist_ok=True)
    commands = []
    def start(seed=None):
        p = subprocess.Popen([str(runner), '--x1'], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        state = json.loads(p.stdout.readline())
        assert state['ok'], state
        if seed is not None:
            state = say(p, f'SEED {seed}')
        return p, state
    def say(p, command, success=True):
        before = time.monotonic()
        p.stdin.write(command+'\n'); p.stdin.flush()
        state = json.loads(p.stdout.readline())
        commands.append({'command': command, 'ok': state['ok'], 'elapsed_s': time.monotonic()-before})
        assert state['ok'] == success, (command, state)
        return state
    def close(p):
        p.stdin.close(); assert p.wait(timeout=20) == 0, p.stderr.read()
    def latest(state, cid):
        return [e for e in state['equipment'] if e['contact']==cid][-1]
    p, initial = start()
    assert initial['automatic'] == 1 and initial['tick'] == 0 and initial['duration'] == 540
    bodies=sum(c[1] not in (1,2) for c in initial['contacts'])
    assert bodies==15 and initial['active']==bodies+1
    first = next(c for c in initial['contacts'] if c[1]==1)
    assert first[3]==18 and first[6] and latest(initial, first[0])['mask']==63
    assert all(s[3]==1 for s in latest(initial, first[0])['slots'])
    before = say(p, 'STEP 59'); assert before['active']==bodies+1
    cargo = say(p, 'STEP 1'); assert cargo['active']==bodies+2
    added = next(c for c in cargo['contacts'] if c[1]==1 and c[0]!=first[0])
    assert added[3]==18 and added[6] and latest(cargo, added[0])['tick']==60
    rom = say(p,'STEP 90'); warbird = next(c for c in rom['contacts'] if c[3]==8)
    e = latest(rom, warbird[0]); assert warbird[6]==0 and e['tick']==150
    assert e['slots'][0][:3]==[8,1,6] and e['slots'][0][3]==2
    changed = say(p,'STEP 60'); e = latest(changed, added[0])
    assert e['tick']==210 and e['slots'][0][0]==1 and e['slots'][0][3]==2
    count = len(changed['equipment'])
    assert len(say(p,'STATUS')['equipment']) == count
    unknown = say(p,'STEP 30'); un = next(c for c in unknown['contacts'] if c[1]==1 and c[3]==0)
    e = latest(unknown, un[0]); assert un[6]==0 and e['class']==0 and e['catalog']==0
    assert e['slots'][0][0]>=6 and e['slots'][1][0]==2 and e['slots'][2][0]==2
    assert not e['mask']&8 and e['slots'][3][:2]==[0,0]
    assert all(s[3]==0 for s in e['slots'])
    assert unknown['deliveries']==[] and unknown['contact_briefs']==[]
    for command in ('REPORT','TACTICAL_SEND','SCIENCE_SEND'):
        state = say(p, f'{command} {un[0]}')
        again = say(p, f'{command} {un[0]}')
        assert state['deliveries']==again['deliveries']
    assert len(state['deliveries'])==3
    assert all(d[2]==e['id'] and d[5]==1 for d in state['deliveries'])
    savepath = output/'checkpoint.aster'
    saved = say(p, f'SAVEFILE {savepath}')
    close(p)
    p, _ = start()
    restored = say(p, f'LOADFILE {savepath}')
    for key in ('tick','contacts','equipment','deliveries','contact_briefs'):
        assert restored[key]==saved[key], (key,restored[key],saved[key])
    assert restored['events']==[], 'restoration must not replay old notices'
    # Duplicated delivery in an entirely new process retains same receipt.
    assert say(p, f'TACTICAL_SEND {un[0]}')['deliveries']==saved['deliveries']
    before = say(p,'STATUS')
    say(p,'SCIENCE_SEND 999999999',False)
    say(p,'STEP malformed',False)
    say(p,'STEP 10junk',False)
    say(p,'RESTART 4junk',False)
    say(p,'RESTART 9',False)
    after = say(p,'STATUS'); assert before['equipment']==after['equipment'] and before['contacts']==after['contacts']
    active = say(p,'STEP 60'); assert latest(active,warbird[0])['slots'][0][3]==3
    hidden = say(p,'STEP 60'); assert hidden['tick']==360 and hidden['active']==bodies+4
    assert len(hidden['latency'])==0, 'restored latency must not invent new arrivals'
    assert len(hidden['contacts'])==bodies+4 and all(c[3]!=18 or c[6] for c in hidden['contacts'])
    revealed = say(p,'STEP 30'); assert revealed['active']==bodies+5
    decloaked = next(c for c in revealed['contacts'] if c[3]==18 and c[6]==0)
    assert latest(revealed,decloaked[0])['tick']==390
    assert all(0 <= l[2] <= l[3] <= l[4] for l in revealed['latency'])
    offline = say(p,'STEP 60'); assert offline['offline']==1 and offline['active']==0
    online = say(p,'STEP 15'); assert online['offline']==0 and online['active']==bodies+5
    ending = say(p,'STEP 75'); assert ending['tick']==540
    assert all(e['contact'] in {c[0] for c in ending['contacts']} for e in ending['equipment'])
    assert all(c[0] not in range(910001,910007) for c in ending['contacts'])
    assert 'world_entity_key' not in json.dumps(ending), 'private keys must not reach public protocol'
    close(p)
    # A changed observation can be deliberately sent again. Retrying the
    # same observation keeps its original receipt, even after fresh-process load.
    p, _ = start()
    state = say(p, 'STEP 60')
    target = next(c[0] for c in state['contacts'] if c[6] == 71002)
    old = say(p, f'TACTICAL_SEND {target}')['deliveries'][0]
    state = say(p, 'STEP 150')
    updated = latest(state, target)
    sent = say(p, f'TACTICAL_SEND {target}')
    assert len(sent['deliveries']) == 2 and sent['deliveries'][-1][2] == updated['id']
    assert sent['deliveries'][-1][0] != old[0]
    assert say(p, f'TACTICAL_SEND {target}')['deliveries'] == sent['deliveries']
    close(p)
    # Same seed/cadence -> same observed equipment; different seeds -> variety.
    projections=[]
    for seed in (42,42,7,11):
        p, state = start(seed); state=say(p,'STEP 240')
        projections.append({k:state[k] for k in ('contacts','equipment')});close(p)
    assert projections[0]==projections[1]
    assert projections[0]!=projections[2] and projections[2]!=projections[3]
    summary={'status':'PASS','mode':'native_ticks_not_MSI_realtime','tests':
             ['T01','T02','T03','T04','T05','T06','T07','T08 plumbing','T09 fresh process',
              'T10 protocol negatives','T12','T13','T14'], 'commands':commands}
    (output/'acceptance.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print('PASS ASTER_X1: autonomous equipment, cloak, fresh-process save/load, receipts, determinism')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--runner',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    a=parser.parse_args();run(a.runner.resolve(),a.output_dir)
