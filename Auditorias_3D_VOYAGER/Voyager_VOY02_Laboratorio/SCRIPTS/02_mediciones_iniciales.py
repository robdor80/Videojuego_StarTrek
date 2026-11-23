import numpy as np,json,collections,csv,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(label):
 d=np.load(R/'DATOS'/f'{label}_geometria.npz');return d['vertices'],d['triangles'],d['object_ids'],json.loads((R/'DATOS'/f'{label}_objetos.json').read_text(encoding='utf8'))
v,t,ids,obs=load('obj');tri=v[t];cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(cross,axis=1)/2;z=tri.mean(axis=1)[:,2];flat=(np.abs(cross[:,2])>.98*np.linalg.norm(cross,axis=1))&(area>1e-6);levels=collections.defaultdict(lambda:collections.Counter())
for k in np.where(flat)[0]:levels[round(z[k],3)][obs[ids[k]]['name']]+=float(area[k])
lev=[{'z':key,'area_abs':sum(a.values()),'objects':dict(a)} for key,a in sorted(levels.items()) if sum(a.values())>.05]
(R/'DATOS/planos_horizontales_obj.json').write_text(json.dumps(lev,indent=2),encoding='utf8')
cand=[]
for o in obs:
 lo=np.array(o['bounds_min']);hi=np.array(o['bounds_max']);sz=hi-lo
 if (min(sz[:2])<.25 and sz[2]>1.45) or o['name'].startswith(('Doorpanel','Box_','Layer__')):
  cand.append({'name':o['name'],'center':((lo+hi)/2).tolist(),'size':sz.tolist(),'materials':o['materials']})
(R/'DATOS/candidatos_accesos_y_muebles.json').write_text(json.dumps(cand,indent=2),encoding='utf8')
mv,mt,mids,mobs=load('modulos');modules=[]
for oi,o in enumerate(mobs):
 lo=np.array(o['bounds_min']);hi=np.array(o['bounds_max']);sz=hi-lo;part=mv[mt[mids==oi]]
 # Raw extreme-plane profiles, in world coordinates, not yet declared functional exits.
 profiles=[]
 for ax in [0,1]:
  for side,coord in [(-1,lo[ax]),(1,hi[ax])]:
   points=part.reshape((-1,3));on=points[np.abs(points[:,ax]-coord)<1e-5];uv=np.delete(on,ax,axis=1);uv=np.unique(np.round(uv,5),axis=0)
   profiles.append({'axis':ax,'side':side,'plane':float(coord),'points_transverse_z':uv.tolist(),'num_points':len(uv)})
 modules.append({**o,'size':sz.tolist(),'extreme_profiles':profiles})
(R/'DATOS/modulos_sondeo.json').write_text(json.dumps(modules,indent=2),encoding='utf8')
# Scale between native MAX conversion and OBJ, using named, independent components.
xv,xt,xids,xobs=load('max');by={o['name']:o for o in obs};xb={o['name']:o for o in xobs};pairs=[]
for a,b in [('Mainroof','Mainroof_1'),('hallwayfloor','hallwayfloor_1'),('centerlight','centerlight_1'),('centerlights01','centerlights_2'),('blackinset','blackinset_1'),('centerinset','centerinset_1'),('lightssupport','lightssupport_1'),('hallwaypanels','hallwaypanels_1'),('hallwaysubframe','hallwaysubframe_1'),('strudextends','strudextends_1')]:
 if a not in xb or b not in by:continue
 A=xb[a];B=by[b];sa=np.array(A['bounds_max'])-A['bounds_min'];sb=np.array(B['bounds_max'])-B['bounds_min'];ratio=np.divide(sa,sb,out=np.full(3,np.nan),where=sb>1e-4);s=float(np.nanmedian(ratio));translation=(np.array(A['bounds_min'])+A['bounds_max'])/2-s*(np.array(B['bounds_min'])+B['bounds_max'])/2
 pairs.append({'max':a,'obj':b,'max_over_obj_xyz':ratio.tolist(),'median_scale':s,'translation_max_minus_scaled_obj':translation.tolist(),'triangles_max':A['triangles'],'triangles_obj':B['triangles']})
(R/'DATOS/comparacion_escala_max_obj.json').write_text(json.dumps(pairs,indent=2),encoding='utf8')
print('LEVELS',[(x['z'],round(x['area_abs'],3),list(x['objects'])[:4]) for x in lev]);print('DOORS',[(o['name'],[round(x,3) for x in o['center']],[round(x,3) for x in o['size']]) for o in cand]);print('PAIRS',pairs)
