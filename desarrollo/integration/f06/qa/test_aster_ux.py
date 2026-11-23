"""Native UX contracts: full chart, real physics, continuous authenticated queues.

Tick-based tests never certify MSI rendering or real-time latency.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import time


def run(runner, output):
    output.mkdir(parents=True, exist_ok=True)
    measurements = []
    def start():
        p = subprocess.Popen([str(runner), '--x1'], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        s = json.loads(p.stdout.readline())
        assert s['ok'], s
        return p, s
    def say(p, cmd, ok=True):
        before = time.monotonic()
        p.stdin.write(cmd+'\n'); p.stdin.flush()
        s = json.loads(p.stdout.readline())
        measurements.append({'command':cmd.split()[0], 'elapsed_s':time.monotonic()-before})
        assert s['ok'] == ok, (cmd, s)
        return s
    def close(p):
        p.stdin.close()
        assert p.wait(timeout=15) == 0, p.stderr.read()
    p, s = start()
    counts = Counter(c[1] for c in s['contacts'] if c[2] == 1)
    assert counts[12] == 1 and counts[13] == 6 and counts[14] == 4 and counts[16] == 1, counts
    assert len(s['science']) == 6 and not s['science_issues']
    assert len(dict(s['chart_labels'])) == 15
    for r in s['science']:
        before = time.monotonic()
        result = say(p, f'SCAN {r[0]}')
        assert time.monotonic()-before < 2 and result['tick'] == 0
        v = next(v for v in result['deep_analysis'] if v['contact'] == r[0])
        assert v['mask'] & 1 and v['science_source'] and v['position_source']
        assert v['oxygen_microbar'] == r[5]*r[8] and v['co2_microbar'] == r[5]*r[9]
        # Planet transfer uses a real completed Core Science report.
        delivered = say(p, f'SCIENCE_SEND {r[0]}')
        assert delivered['deliveries'][-1][2] == v['science_source']
        assert say(p, f'SCIENCE_SEND {r[0]}')['deliveries'] == delivered['deliveries']
    s = say(p, 'STEP 150')
    rom = next(c for c in s['contacts'] if c[1] == 1 and c[3] == 8)
    s = say(p, f'PRIORITY {rom[0]}')
    assert any(d[1] == rom[0] and d[4] == 2 and d[5] == 1 for d in s['deliveries'])
    baseline = len(s['deliveries'])
    say(p, f'REPORT {rom[0]}')
    s = say(p, 'STEP 10')
    assert len(s['deliveries']) > baseline
    positions = {r[0]:r for r in s['position_evidence']}
    position_deliveries = [d for d in s['deliveries'] if d[1] == rom[0] and d[2] in positions]
    assert position_deliveries and positions[position_deliveries[-1][2]][2] >= 155
    assert any(n[0] == rom[0] and n[6] > 0 for n in s['navigation'])
    updated_report=say(p, f'REPORT {rom[0]}')
    maneuver_reports=[d for d in updated_report['deliveries'] if d[1]==rom[0] and d[4]==1]
    assert len(maneuver_reports)==2 and maneuver_reports[-1][2] in {r[0] for r in updated_report['position_evidence']}
    assert say(p, f'REPORT {rom[0]}')['deliveries']==updated_report['deliveries']
    checkpoint = output/'tracking.aster'
    saved = say(p, f'SAVEFILE {checkpoint}')
    close(p)
    p, _ = start()
    restored = say(p, f'LOADFILE {checkpoint}')
    assert restored['tracking'] == saved['tracking'] and restored['deliveries'] == saved['deliveries']
    s = say(p, 'STEP 140')
    offensive = [e for e in s['equipment'] if e['contact'] == rom[0]][-1]
    assert offensive['tick'] == 300 and offensive['slots'][0][1] == 3
    assert any(d[2] == offensive['id'] and d[4] == 2 and d[5] == 1 for d in s['deliveries'])
    first = say(p, f'REPORT {rom[0]}')['deliveries'][-1]
    s = say(p, 'STEP 120')
    latest = [e for e in s['equipment'] if e['contact'] == rom[0]][-1]
    assert latest['slots'][0][1] == 1 and latest['tick'] == 420
    sent = say(p, f'REPORT {rom[0]}')
    assert sent['deliveries'][-1][2] == latest['id'] and sent['deliveries'][-1][0] != first[0]
    assert say(p, f'REPORT {rom[0]}')['deliveries'] == sent['deliveries']
    assert all(d[2] in {e['id'] for e in s['equipment']} | set(positions) |
               {r[0] for r in s['position_evidence']} |
               {v['science_source'] for v in s['deep_analysis']} for d in s['deliveries'])
    s = say(p, f'UNFOLLOW {rom[0]}')
    n = len(s['deliveries'])
    assert next(r[1] for r in s['tracking'] if r[0] == rom[0]) == 0
    assert len(say(p, 'STEP 10')['deliveries']) == n
    say(p, 'SCAN 99999999', False)
    negative = say(p, 'STATUS')
    assert len(negative['deliveries']) == n
    close(p)
    (output/'ux-contract.json').write_text(json.dumps({'status':'PASS', 'measurements':measurements}, indent=2))
    print('PASS full Aster, immediate physical analysis, Science queue, continuous Tactical, fresh process, updates')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    run(args.runner.resolve(), args.output_dir)
