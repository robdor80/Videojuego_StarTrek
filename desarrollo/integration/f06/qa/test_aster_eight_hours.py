"""Independent eight-hour Core regression at ×15/×30/×60 command cadences.
Executes native ticks as fast as possible; no claim of real-time latency.
"""
import argparse
import json
from pathlib import Path
import subprocess
import time


def run(runner, output):
    output.mkdir(parents=True,exist_ok=True)
    results=[]
    for speed in (15,30,60):
        started=time.monotonic()
        p=subprocess.Popen([str(runner)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,text=True)
        state=json.loads(p.stdout.readline());assert state['ok']
        for _ in range(0,28800,speed):
            p.stdin.write(f'STEP {speed}\n');p.stdin.flush()
            state=json.loads(p.stdout.readline());assert state['ok'],state
        assert state['tick']==28800 and state['automatic']==1 and state['active']>=15
        assert any(c[3]==8 and c[2]==1 for c in state['contacts'])
        assert any(e['class']==8 and e['slots'][0][0]==8 and e['slots'][0][3]==2
                   for e in state['equipment'])
        assert state['deliveries']==[],'no automatic official reports or transfers'
        p.stdin.close();assert p.wait(timeout=20)==0,p.stderr.read()
        results.append({'cadence_multiplier':speed,'core_seconds':state['tick'],
                        'wall_s':time.monotonic()-started,'equipment_observations':len(state['equipment'])})
    (output/'eight-hours.json').write_text(json.dumps(results,indent=2))
    print('PASS separate eight-hour Core regressions: ×15 / ×30 / ×60 cadence; not ×1 latency evidence')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--runner',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    run(a.runner.resolve(),a.output_dir)
