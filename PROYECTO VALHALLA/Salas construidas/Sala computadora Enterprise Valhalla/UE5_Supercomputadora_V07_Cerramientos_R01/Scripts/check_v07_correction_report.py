"""Check authored cold approaches, threshold crossings, occupation, cycles and every expected functional case."""
import argparse,json,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--plan',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
plan=json.loads(a.plan.read_text(encoding='utf-8-sig'))['cases'];report=json.loads(a.report.read_text(encoding='utf-8-sig'));assert len({r['name'] for r in plan})==len(plan)
assert report['capsule_radius_cm']==35 and report['capsule_half_height_cm']==90 and 'Quinn' in report['mesh']
assert 'EnhancedInput' in report['player_input_class']
rows={r['name']:r for r in report['results']};scripts=Path(__file__).resolve().parent
inner=json.loads((scripts/'v07_inner_accesses.json').read_text());axes={'V07_'+r['id']:(r['root'],r['yaw']) for r in inner}
for r in json.loads((scripts/'v07_memory_accesses.json').read_text(encoding='utf-8-sig')):
 yaw=r['outward_yaw'];t=math.radians(yaw);c=r['wall_face_center_cm'];axes[r['id']]=([c[0]-20*math.cos(t),c[1]-20*math.sin(t),37],yaw)
results=[]
for case in plan:
 r=rows.get(case['name']);issues=[]
 if not r or not r['passed']:issues.append('missing_or_failed_runtime_case')
 else:
  if r['falling']:issues.append('ended_without_ground_support')
  if case.get('min_closed_cycles',0)>r.get('completed_close_cycles',0):issues.append('incomplete_close_cycles')
  if case.get('door_min',0)>.99 and not (r['door_fraction']>.99 and r['door_occupied']):issues.append('occupation_did_not_hold_door_open')
  if case.get('expect_blocked') and r['waypoints_reached']>=len(case['points']):issues.append('crossed_expected_boundary')
  if any(s in case['name'] for s in ('entrada_fria','salida_fria','aproximacion_fria')):
   root,yaw=axes[case['door_id']];t=math.radians(yaw);trace=r['trace']+[r]
   xs=[(s['feet_cm'][0]-root[0])*math.cos(t)+(s['feet_cm'][1]-root[1])*math.sin(t) for s in trace]
   if min(xs)>-50 or max(xs)<50:issues.append('no_physical_threshold_crossing_observed')
   if max(s['door_fraction'] for s in trace)<.999:issues.append('door_never_fully_opened')
   if any(s['feet_cm'][2]<36.9 for s in trace):issues.append('fell_below_constructed_floor')
   if max(max(s.get('left_path_error_cm',0),s.get('right_path_error_cm',0)) for s in trace)>.05:issues.append('leaf_did_not_follow_real_slide_path')
 results.append(dict(name=case['name'],ok=not issues,issues=issues))
out=dict(ok=all(r['ok'] for r in results),passed=sum(r['ok'] for r in results),total=len(results),results=results)
assert not a.output.exists();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2),encoding='utf8')
print(out['passed'],'/',out['total'],[r for r in results if not r['ok']]);raise SystemExit(0 if out['ok'] else 1)
