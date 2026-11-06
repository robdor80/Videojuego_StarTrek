import json,sys,math,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Matrix,Quaternion,Vector
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--geometry',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
assert not args.output.exists()
args.output.parent.mkdir(parents=True,exist_ok=True)
scripts=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('geom',scripts/'build_v07_memory_geometry.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
data=json.loads((args.geometry).read_text())
out=dict(v07_correction=True,materials={},doors=[])
for k in range(273,281):
 path=f'/Game/Valhalla/Meshes/SM_{k}.SM_{k}'
 rows=[r for r in data['instances'] if r['mesh']==path];assert len(rows)==1
 r=rows[0];m=data['meshes'][path];q=r['rotation'];T=Matrix.LocRotScale(Vector(r['location']),Quaternion((q[3],*q[:3])),Vector(r['scale']))
 verts=np.array([T@Vector(v) for v in m['vertices']]);ev,evec=np.linalg.eigh(np.cov(verts[:,:2].T));normal=evec[:,0]
 cy=-1431.4359665 if k<277 else 1926.18515
 center=(verts.min(0)+verts.max(0))/2;center[2]=verts[:,2].min()
 if np.dot(normal,center[:2]-np.array([2268.4833,cy]))<0:normal=-normal
 yaw=math.degrees(math.atan2(normal[1],normal[0]));a=math.radians(yaw);R=np.array([[math.cos(a),math.sin(a),0],[-math.sin(a),math.cos(a),0],[0,0,1]])
 local=(verts-center)@R.T
 nm=np.array(T.to_3x3().inverted().transposed())
 record=dict(id=f'SRV_R{1 if k<277 else 2}_Q{(k-273)%4+1}',root=center.tolist(),yaw=yaw,original_asset=path,original_location=r['location'],original_rotation=r['rotation'],original_scale=r['scale'],width=float(np.ptp(local[:,1])),height=float(np.ptp(local[:,2])),leaves=[])
 source_area=0
 for sign in (-1,1):
  part=g.new_part('leaf')
  for tri in m['triangles']:
   ns=np.array(tri['n'])@nm.T@R.T
   poly=[np.r_[local[v],uv,n] for v,uv,n in zip(tri['v'],tri['uv'],ns)]
   if sign<0:source_area+=g.area(poly)
   piece=g.half(poly,1,0,sign<0)
   g.emit(part,piece,m['materials'][tri['material']])
  vs=np.array(part['vertices']);pivot=(vs.min(0)+vs.max(0))/2
  part['vertices']=(vs-pivot).tolist()
  record['leaves'].append(dict(closed=pivot.tolist(),mesh=part))
  out['materials'].update({mat:mat for mat in part['materials']})
 def area(p):
  v=np.array(p['vertices']);return sum(np.linalg.norm(np.cross(v[t['v'][1]]-v[t['v'][0]],v[t['v'][2]]-v[t['v'][0]]))/2 for t in p['triangles'])
 record['surface_area_error_cm2']=abs(source_area-sum(area(leaf['mesh']) for leaf in record['leaves']));assert record['surface_area_error_cm2']<.01
 record['travel']=record['width']/2+7
 out['doors'].append(record)
(args.output).write_text(json.dumps(out,separators=(',',':')))
(args.output.with_name(args.output.stem+'_positions.json')).write_text(json.dumps([{k:r[k] for k in ('id','root','yaw','width','height','travel','surface_area_error_cm2')} for r in out['doors']],indent=2))
print([(r['id'],round(r['width'],3),round(r['height'],3),r['surface_area_error_cm2']) for r in out['doors']])
