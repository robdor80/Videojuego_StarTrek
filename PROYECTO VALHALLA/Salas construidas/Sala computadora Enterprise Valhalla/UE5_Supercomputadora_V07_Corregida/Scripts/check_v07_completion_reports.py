"""Verify the final plan against ordered runtime reports (later repeats supersede earlier cases)."""
import argparse
import json
import math
from pathlib import Path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--plan',required=True)
    parser.add_argument('--output',required=True);parser.add_argument('reports',nargs='+')
    args=parser.parse_args()
    expected=json.loads(Path(args.plan).read_text())['cases'];latest={}
    for path in args.reports:
        report=json.loads(Path(path).read_text())
        assert report['capsule_radius_cm']==35 and report['capsule_half_height_cm']==90
        assert 'Quinn' in report['mesh']
        for row in report['results']:latest[row['name']]=row
    accesses=json.loads(Path(__file__).with_name('v07_memory_accesses.json').read_text(encoding='utf-8-sig'))
    coordinates={r['id']:r for r in accesses};results=[]
    for case in expected:
        row=latest.get(case['name']);issues=[]
        if not row or not row['passed']:issues.append('missing_or_failed_runtime_case')
        elif case['name'].startswith('MEM_'):
            config=coordinates[case['door_id']];angle=math.radians(config['outward_yaw'])
            def local_x(sample):
                x,y,_=sample['feet_cm'];cx,cy,_=config['wall_face_center_cm']
                return (x-cx)*math.cos(angle)+(y-cy)*math.sin(angle)+20
            trace=row['trace']+[row]
            if any(s['feet_cm'][2]<36.9 for s in trace):issues.append('feet_below_floor')
            if case['name'].endswith('_seguridad') and any(local_x(s)>-30 for s in trace):issues.append('crossed_locked_door')
            if case['name'].endswith('_ocupacion') and not (row['door_occupied'] and row['door_fraction']>=.999):issues.append('occupation_not_held')
            if case['name'].endswith(('_entrada','_salida')):
                xs=[local_x(s) for s in trace]
                if min(xs)>-50 or max(xs)<50:issues.append('no_threshold_crossing_observed')
                if max(s['door_fraction'] for s in trace)<.999:issues.append('never_fully_opened')
            if case['name'].endswith('_ciclos') and row.get('completed_close_cycles',0)<6:issues.append('incomplete_cycles')
        results.append(dict(name=case['name'],ok=not issues,issues=issues))
    out=dict(ok=all(r['ok'] for r in results),passed=sum(r['ok'] for r in results),total=len(results),results=results)
    Path(args.output).write_text(json.dumps(out,indent=2),encoding='utf8')
    print(out['passed'],'/',out['total'],[r for r in results if not r['ok']])
    if not out['ok']:raise SystemExit(1)


if __name__=='__main__':main()
