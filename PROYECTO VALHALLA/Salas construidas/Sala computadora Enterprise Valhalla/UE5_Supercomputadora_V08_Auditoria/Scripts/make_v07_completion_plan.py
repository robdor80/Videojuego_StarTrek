"""Generate Quinn traversal and safety cases; --output is a temporary evidence path."""
import argparse
import json
import math
from pathlib import Path


def make_plan(captures=None):
    rows=json.loads(Path(__file__).with_name('v07_memory_accesses.json').read_text(encoding='utf-8-sig'))
    cases=[]
    for row in rows:
        yaw=math.radians(row['outward_yaw']);x,y,_=row['wall_face_center_cm']
        def p(a,b=0):
            return [x+(a-20)*math.cos(yaw)-b*math.sin(yaw),
                    y+(a-20)*math.sin(yaw)+b*math.cos(yaw),37]
        common=dict(door_id=row['id'],yaw=row['outward_yaw'],seconds=12)
        lateral=100 if row.get('connects_existing_corridor',False) else 280
        entry=dict(common,name=row['id']+'_entrada',start=p(-180),points=[p(310)])
        if captures:
            entry.update(screenshot=str(Path(captures).resolve()/(row['id']+'_abierta.png')),capture_at=p(80))
        cases += [entry,dict(common,name=row['id']+'_salida',start=p(310),points=[p(-180)]),
                  dict(common,name=row['id']+'_ocupacion',start=p(-160),points=[p(0)],hold=True,seconds=5,door_min=.999),
                  dict(common,name=row['id']+'_seguridad',start=p(-160),points=[p(100)],locked=True,
                       expect_blocked=True,seconds=4,door_max=.001),
                  dict(common,name=row['id']+'_fondo_seguro',start=p(310),points=[p(520)],
                       expect_blocked=True,seconds=4,expect_actor_prefix=row['id']+'_Enclosure'),
                  dict(common,name=row['id']+'_lateral_izquierdo',start=p(lateral),points=[p(lateral,-200)],
                       expect_blocked=True,seconds=4,expect_actor_prefix=row['id']+'_Enclosure'),
                  dict(common,name=row['id']+'_lateral_derecho',start=p(lateral),points=[p(lateral,200)],
                       expect_blocked=True,seconds=4,expect_actor_prefix=row['id']+'_Enclosure'),
                  dict(common,name=row['id']+'_ciclos',start=p(-260),
                       points=[p(310),p(-260)]*3,waypoint_waits=[3.3]*6,
                       hold=True,seconds=40,min_closed_cycles=6)]
        if row.get('connects_existing_corridor',False):
            next(c for c in cases if c['name']==row['id']+'_fondo_seguro').pop('expect_actor_prefix')
    # Existing B08 fall-regression cases remain applicable; memory closures do not.
    closure=json.loads(Path(__file__).with_name('v07_closure_plan.json').read_text())
    cases += [r for r in closure['cases'] if not r['name'].startswith('MEM_')]
    return dict(cases=cases)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    parser.add_argument('--captures');args=parser.parse_args()
    Path(args.output).write_text(json.dumps(make_plan(args.captures),indent=2),encoding='utf8')
