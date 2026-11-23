"""Explicit seated diagnostic proxy, exact external-surface distances, no population fit claim."""
import sys,json,math
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import *
v,t,ids,obs=load('obj');tri=v[t]*1.1;names=np.array([o['name'] for o in obs]);by={o['name']:i for i,o in enumerate(obs)}
erg=json.loads((R/'DATOS/ergonomia_detallada.json').read_text());fun=json.loads((R/'DATOS/preparacion_funcional.json').read_text());groups={c['id']:list(c['parts']) for c in fun['chairs']}
groundmask=np.isin(ids,[i for i,o in enumerate(obs) if 'Voygray' in o['materials'] or o['name'] in ['Mesh_1856','Mesh_1787','Object_75']]);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);groundmask&=np.abs(cross[:,2])>.98*np.linalg.norm(cross,axis=1);ground=tri[groundmask]
groups['NAVEGACION']=[n for n in groups['NAVEGACION'] if n not in ['Object_75','Object_126','Object_127','Object_129']]
groups['MANDO_IZQ']+=['ChamferBox_'+str(i) for i in range(23,30)];groups['MANDO_DER']+=['ChamferBox_'+str(i) for i in range(30,37)]
backparts={'NAVEGACION':'Layer__3','LATERAL_DER':'Layer__4','LATERAL_IZQ':'Layer__5','MANDO_IZQ':'Box_7','MANDO_DER':'Box_9'}
def capsule_segment_dist(tri,p,q,r):
 # Align an arbitrary segment with Z and reuse tested exact segment-triangle method.
 p=np.array(p);q=np.array(q);axis=q-p;length=np.linalg.norm(axis);z=axis/max(length,1e-15);seed=np.array([1.,0,0]) if abs(z[0])<.8 else np.array([0.,1,0]);x=np.cross(seed,z);x/=np.linalg.norm(x);y=np.cross(z,x);rot=np.stack([x,y,z],axis=1);local=(tri-p)@rot
 return capsule_distance(local,[0,0,-r],height=length+2*r,radius=r)-r
out=[]
for seat in erg['seats']:
 name=seat['id'];pts=np.array(seat['sample_points_m']);xy=pts[:,:2].mean(axis=0);z=seat['seat_sample_median_z'];b=obs[by[backparts[name]]];back=(np.array(b['bounds_min'])+b['bounds_max'])[:2]*.55;forward=xy-back;forward/=np.linalg.norm(forward);side=np.array([-forward[1],forward[0]])
 mask=~np.isin(names[ids],groups[name]);context=tri[mask];cn=names[ids][mask];variants=[]
 for h in [1.6,1.75,1.9]:
  def at(fwd=0,lat=0,zz=0):return np.array([*(xy+forward*fwd+side*lat),zz])
  hip=at(zz=z+.075);shoulder=at(zz=z+.32*h);eyes=at(.035,zz=z+.46*h);headtop=z+.52*h;limbs=[('TORSO',hip,shoulder,.12),('CABEZA',eyes,at(.035,zz=headtop-.06),.095)]
  feet=[]
  for sign in [-1,1]:
   hp=at(lat=sign*.10,zz=z+.07);knee=at(.245*h,sign*.10,z+.07);ankle=at(.245*h,sign*.10,z+.07-.245*h);limbs.extend([('MUSLO_'+str(sign),hp,knee,.065),('PIERNA_'+str(sign),knee,ankle,.045)]);ff=floor(ground,*ankle[:2],start=.90,limit=2);feet.append(dict(ankle=ankle.tolist(),predicted_sole_z_m=float(ankle[2]-.07),sole_gap_to_reference_floor_m=float(ankle[2]-.07-seat['floor']['point'][2]) if seat['floor'] else None,actual_floor_under_foot=ff,sole_gap_to_local_floor_m=float(ankle[2]-.07-ff['point'][2]) if ff else None))
  checks=[]
  for label,p,q,r in limbs:
   lo=np.minimum(p,q)-r;hi=np.maximum(p,q)+r;near=(context.max(axis=1)>=lo).all(axis=1)&(context.min(axis=1)<=hi).all(axis=1);ix=np.where(near)[0]
   dist=capsule_segment_dist(context[ix],p,q,r) if len(ix) else np.array([]);bad=ix[dist<-1e-5];checks.append(dict(part=label,p_m=p.tolist(),q_m=q.tolist(),radius_m=r,external_surface_clear=not len(bad),minimum_clearance_m=float(dist.min()) if len(dist) else None,blocking_objects=sorted(set(cn[bad].tolist()))))
  targets=[]
  for scr in erg['screens']:
   center=np.array(scr['center_m']);delta=center[:2]-xy;length=np.linalg.norm(delta)
   if length>1.5 or np.dot(delta,forward)<.25*length:continue
   shoulderpoint=shoulder+np.array([*(side*(.18 if np.dot(delta,side)>0 else -.18)),0]);distance=float(np.linalg.norm(center-shoulderpoint));targets.append(dict(object=scr['object'],surface_center_m=center.tolist(),shoulder_distance_m=distance,within_hypothetical_arm_length=distance<=.38*h,arm_length_hypothesis_m=.38*h,note='Center target only; no joint angle, line of sight or hand task certification.'))
  variants.append(dict(height_m=h,limb_tests=checks,feet=feet,eyes_m=eyes.tolist(),head_top_m=headtop,control_center_candidates=targets))
 out.append(dict(id=name,refined_parts=groups[name],forward_xy=forward.tolist(),seat_reference_m=[*xy,z],variants=variants,grade='C',semantic_review='Navigation excludes fixed platform and 3 console pieces; command adds fabric cushions/back pads omitted by prior four-part shell grouping. No animation rig certified.'))
 print('POSTURE',name,[(p['height_m'],sum(not t['external_surface_clear'] for t in p['limb_tests'])) for p in variants],flush=True)
(R/'DATOS/puestos_revision.json').write_text(json.dumps(dict(scale=1.1,stations=out,proxy_parameters=dict(thigh_length_fraction=.245,lower_leg_length_fraction=.245,hip_above_seat_m=.07,shoulder_height_fraction=.32,seated_eye_height_fraction=.46,seated_top_fraction=.52,arm_length_fraction=.38),method='Three unvalidated parametric body sizes, separate limb capsules vs all external triangles; own-chair contact excluded explicitly. Hypotheses are not ANSUR percentile values or a validated humanoid rig. Negative contacts and foot gaps identify adaptation needs; clean proxies cannot approve comfort, vision, reach or sit/stand.',source_review='OSHA feet/support and adjustability principles; NASA task-specific fit/reach/view principles, no numerical anthropometric percentile claims.'),indent=2,ensure_ascii=False),encoding='utf8')
