import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from geom import *
from mathutils.kdtree import KDTree
ov,ot,oi,oo=load('obj');mv,mt,mi,mo=load('max');s=1.50813535;offset=np.array([-.11236,1.875563,-.466607])
oc=np.array([(np.array(o['bounds_min'])+o['bounds_max'])/2 for o in oo]);od=np.array([np.array(o['bounds_max'])-o['bounds_min'] for o in oo]);rows=[]
for k,o in enumerate(mo):
 if o['name']=='Voyager Bridge' or not o['triangles']:continue
 c=((np.array(o['bounds_min'])+o['bounds_max'])/2-offset)/s;d=(np.array(o['bounds_max'])-o['bounds_min'])/s;err=np.linalg.norm(oc-c,axis=1)+np.linalg.norm(od-d,axis=1);j=int(err.argmin());rows.append({'max':o['name'],'parent_max':o['parent'],'obj':oo[j]['name'],'bbox_error_m':float(err[j]),'candidate':bool(err[j]<.002)})
prior=json.loads((R.parent/'Voyager_Puente_2026-10-21/DATOS/blender_recovery.json').read_text(encoding='utf8'));parents={o['name']:o['parent'] for o in prior['objects']}
def ancestor(name):
 a=[]
 while name in parents and parents[name]:name=parents[name];a.append(name)
 return a
groups={}
for group in ['door3','door4','door04','door05','door06','door07','Group009','Group008','Group003']:
 groups[group]=[r for r in rows if group in ancestor(r['max']) or r['parent_max']==group]
# Nearest-vertex residuals for independent, confidently corresponding architectural parts.
checks=[]
for a,b in [('Mainroof','Mainroof_1'),('hallwayfloor','hallwayfloor_1'),('centerlight','centerlight_1'),('centerlights01','centerlights_2'),('blackinset','blackinset_1'),('centerinset','centerinset_1'),('lightssupport','lightssupport_1'),('hallwaypanels','hallwaypanels_1'),('hallwaysubframe','hallwaysubframe_1'),('strudextends','strudextends_1')]:
 ka=next(k for k,o in enumerate(mo) if o['name']==a);kb=next(k for k,o in enumerate(oo) if o['name']==b);pa=np.unique(mv[mt[mi==ka]].reshape((-1,3)),axis=0);pb=np.unique(ov[ot[oi==kb]].reshape((-1,3)),axis=0);pa=(pa-offset)/s;tree=KDTree(len(pb))
 for j,p in enumerate(pb):tree.insert(p,j)
 tree.balance();ds=np.array([tree.find(p)[2] for p in pa]);checks.append({'max':a,'obj':b,'sample_vertices_max':len(pa),'rms_m':float(np.sqrt((ds*ds).mean())),'p95_m':float(np.quantile(ds,.95)),'max_m':float(ds.max()),'grade':'A' if ds.max()<.001 else 'E'})
out={'obj_to_max_scale':s,'obj_to_max_translation':offset.tolist(),'matching':rows,'functional_groups':groups,'scale_checks':checks,'explanation':'Empirical uniform similarity on independent matching architecture. Does not establish original author units; local transform/topology exceptions preserved.'}
(R/'DATOS/correspondencias_max_obj.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print('MATCHED',sum(r['candidate'] for r in rows),'of',len(rows))
for g,rs in groups.items():print(g,[(r['max'],r['obj'],round(r['bbox_error_m'],5)) for r in rs])
print('CHECKS',checks)
