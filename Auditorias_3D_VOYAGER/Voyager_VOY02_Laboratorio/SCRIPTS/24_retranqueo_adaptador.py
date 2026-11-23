"""Repair a local diagnostic adapter only; preserve previous numerical evidence."""
import bpy,ast,json,sys,shutil,hashlib
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import *
P=R/'DATOS';proto=json.loads((P/'prototipo_conjunto.json').read_text());assert not proto.get('adapter_revision'),'Already revised'
for name in ['prototipo_conjunto.json','prototipo_geometria.npz','encuentros_adaptadores.json']:
 dest=R/'TRASPASO'/('ANTES_RETRANQUEO_'+name);assert not dest.exists();shutil.copy2(P/name,dest)
parsed=ast.parse((R/'SCRIPTS/09_prototipo.py').read_text());exec(compile(ast.Module(body=[x for x in parsed.body if isinstance(x,ast.FunctionDef) and x.name=='solid_quad'],type_ignores=[]),'solid_quad','exec'))
a=next(a for a in proto['adapters'] if a['id']=='AD_PUENTE');old=np.array(a['triangles']);setback=.14;start=np.array(a['start'])+np.array(a['normal'])*setback;end=np.array(a['end']);tan=np.array([-a['normal'][1],a['normal'][0],0.]);z=np.array([0,0,1.]);A=start-tan*a['widthA']/2;B=start+tan*a['widthA']/2;C=end+tan*a['widthB']/2;D=end-tan*a['widthB']/2
new=np.vstack([old[:12],solid_quad(A,D,D+z*a['heightB'],A+z*a['heightA'],-tan*.08),solid_quad(B,B+z*a['heightA'],C+z*a['heightB'],C,tan*.08),solid_quad(A+z*a['heightA'],D+z*a['heightB'],C+z*a['heightB'],B+z*a['heightA'],z*.06)])
a['triangles']=new.tolist();a['wall_roof_setback_m']=setback;a['note']='Revision: floor retained from Y=0, walls/roof start Y=+0.14m behind measured rear-frame maximum ~0.135m. Door leaves remain unchanged. The ~5mm constructive seam needs artistic/local finishing; not a watertight room certificate.'
data=np.load(P/'prototipo_geometria.npz');full=data['triangles'].copy();labels=data['labels'];full[labels=='AD_PUENTE']=new;cc=Collision(full,labels)
for test in proto['routes']:
 route=test['routes'][0]['points'];test['routes']=[cc.path(route,h,.35,.025,.0125) for h in [1.6,1.75,1.9]];test['support']=support_path(full,route);print('REVISED_ROUTE',test['id'],[(r['height'],r['clear'],r['samples']) for r in test['routes']],test['support']['clear'],flush=True)
proto['adapter_revision']=dict(id='R1_RETRANQUEO_140MM',reason='Transverse contacts between flared AD_PUENTE and full rear leaves at static open pose.',previous='TRASPASO/ANTES_RETRANQUEO_prototipo_conjunto.json',scope='Only walls/roof of new AD_PUENTE; source bridge, leaf transforms, modules, floor and furniture unchanged.')
(P/'prototipo_conjunto.json').write_text(json.dumps(proto,indent=2,ensure_ascii=False),encoding='utf8');np.savez_compressed(P/'prototipo_geometria.npz',triangles=full,labels=labels)
path=R/'ESCENAS/VOY02_Laboratorio.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);changed=[]
for scene in bpy.data.scenes:
 for o in scene.objects:
  if o.type=='MESH' and o.name.split('.')[0]=='AD_PUENTE':
   me=bpy.data.meshes.new(o.data.name+'_RETRANQUEO_R1');me.from_pydata(new.reshape((-1,3)).tolist(),[],np.arange(len(new)*3).reshape((-1,3)).tolist());me.materials.append(o.data.materials[0]);me.update();o.data=me;o['VOY02_ADAPTADOR_REVISION']='R1_RETRANQUEO_140MM';o['VOY02_INSTANCE']='AD_PUENTE';changed.append(dict(scene=scene.name,object=o.name))
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(path));(P/'retranqueo_adaptador.json').write_text(json.dumps(dict(setback_m=setback,changed_objects=changed,geometry_new_only=True,door_mechanism_certified=False,blend_sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2),encoding='utf8')
assert len(changed)==2,changed
