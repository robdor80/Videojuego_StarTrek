import json,math,importlib.util,sys
from pathlib import Path
import numpy as np
from mathutils import Matrix,Quaternion,Vector
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--geometry',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--doors',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
assert not args.output.exists()
args.output.parent.mkdir(parents=True,exist_ok=True)
scripts=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('geom',scripts/'build_v07_memory_geometry.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
data=json.loads((args.geometry).read_text());doors=json.loads((args.doors).read_text())['doors'];frames=[]
for r in doors:
 T=Matrix.Translation(Vector(r['root']))@Matrix.Rotation(math.radians(r['yaw']),4,'Z');frames.append((r,T,T.inverted()))
out=dict(v07_correction=True,parts=[],remove=[],direct_replacements=[],materials=[],metrics=[])
for ri,row in enumerate(data['instances']):
 if any(row['mesh']==d['original_asset'] for d in doors):continue
 if row['index']<0 and not row['mesh'].endswith('_Architecture.'+row['mesh'].split('.')[-1]):continue
 # Direct completion meshes are in world space; other direct actors are protected.
 if row['index']<0 and '_Architecture' not in row['mesh']:continue
 mesh=data['meshes'][row['mesh']];q=row['rotation'];T=Matrix.LocRotScale(Vector(row['location']),Quaternion((q[3],*q[:3])),Vector(row['scale']));m=np.array(T);world=np.array(mesh['vertices'])@m[:3,:3].T+m[:3,3]
 lo,hi=world.min(0),world.max(0);candidates=[]
 for d,frame,inv in frames:
  root=np.array(d['root'])
  if np.any(lo>root+[180,180,200]) or np.any(hi<root+[-180,-180,0]):continue
  a=np.array(inv);local=world@a[:3,:3].T+a[:3,3];l,h=local.min(0),local.max(0);half=d['width']+10
  if all(l[k]<[6,half,d['height']+.2][k] and h[k]>[-6,-half,.05][k] for k in range(3)):candidates.append((d,frame,inv))
 if not candidates:continue
 normal=np.array(T.to_3x3().inverted().transposed());polys=[]
 for tr in mesh['triangles']:
  ns=np.array(tr['n'])@normal.T;polys.append(([np.r_[world[v],uv,n] for v,uv,n in zip(tr['v'],tr['uv'],ns)],mesh['materials'][tr['material']]))
 removed=0
 for d,frame,inv in candidates:
  nextpolys=[];a=np.array(inv)
  for poly,mat in polys:
   local=[np.r_[np.array(inv@Vector(c[:3])),c[3:5],a[:3,:3]@c[5:8]] for c in poly]
   keep,cut=g.subtract_box(local,((0,-6,6),(1,-d['width']-10,d['width']+10),(2,.05,d['height']+.2)))
   removed+=max(0,g.area(local)-sum(g.area(p) for p in keep))
   for p in keep:
    nextpolys.append(([np.r_[np.array(frame@Vector(c[:3])),c[3:5],np.array(frame.to_3x3())@c[5:8]] for c in p],mat))
  polys=nextpolys
 if removed<.01:continue
 part=g.new_part(f'V07C_Pocket_{len(out["parts"]):02d}_Architecture')
 for poly,mat in polys:g.emit(part,poly,mat)
 if not part['triangles']:
  assert row['index']>=0,'Do not discard direct architecture actors'
  out['remove'].append(row)
  out['metrics'].append(dict(source=row['mesh'],removed_surface_cm2=removed,fully_inside_leaf_pocket=True))
  continue
 out['parts'].append(part);out['metrics'].append(dict(source=row['mesh'],source_actor=row['actor'],removed_surface_cm2=removed,doors=[r[0]['id'] for r in candidates]))
 if row['index']>=0:out['remove'].append(row)
 else:out['direct_replacements'].append(dict(source=row,target=part['name']))
out['materials']=sorted({mat for p in out['parts'] for mat in p['materials']})
(args.output).write_text(json.dumps(out,separators=(',',':')))
(args.output.with_name(args.output.stem+'_metrics.json')).write_text(json.dumps(out['metrics'],indent=2))
print('POCKETS',len(out['parts']),len(out['remove']),len(out['direct_replacements']))
