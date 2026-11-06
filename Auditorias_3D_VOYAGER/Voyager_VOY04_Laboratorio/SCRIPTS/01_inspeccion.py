import bpy,json,math,sys,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'REFERENCIAS/VOY03_Circulacion.blend'),load_ui=False,use_scripts=False)
s=bpy.data.scenes['01_REFERENCIA_ORIGINAL'];bpy.context.window.scene=s
T=Vector(json.loads((R/'REFERENCIAS/prototipo_conjunto.json').read_text())['bridge_translation'])
manifest=json.loads((R/'REFERENCIAS/manifest_blender.json').read_text()); names=set(manifest['architecture_fingerprints'])
geo=[o for o in s.objects if o.name in names];rows=[];verts=[];tris=[];ids=[]
for i,o in enumerate(geo):
 o.data.calc_loop_triangles();v=np.array([o.matrix_world@p.co-T for p in o.data.vertices]);f=np.array([list(t.vertices) for t in o.data.loop_triangles],int)
 src=str(o.get('VOY02_ORIGEN',''));key=src.removeprefix('OBJ:')
 rows.append(dict(index=i,name=o.name,source=src,key=key,vertices=len(v),triangles=len(f),lo=v.min(0).tolist(),hi=v.max(0).tolist(),matrix=[list(r) for r in o.matrix_world],materials=[m.name if m else None for m in o.data.materials],mesh=o.data.name,users=o.data.users))
 tris.extend((f+len(verts)).tolist());verts.extend(v.tolist());ids.extend([i]*len(f))
np.savez_compressed(R/'DATOS/geometria.npz',vertices=np.array(verts),triangles=np.array(tris),object_ids=np.array(ids))
(R/'DATOS/objetos.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
stations=json.loads((R/'REFERENCIAS/puestos_revision.json').read_text())['stations']
print('SCENES',[(x.name,len(x.objects)) for x in bpy.data.scenes],flush=True)
print('GEOMETRY',len(geo),'ARMATURES',[(o.name,o.type) for o in bpy.data.objects if o.type=='ARMATURE'],flush=True)
for st in stations:
 print('STATION',st['id'],flush=True)
 for r in rows:
  if r['key'] in st['refined_parts']:print(r['key'],np.round(r['lo'],4).tolist(),np.round(r['hi'],4).tolist(),r['materials'],flush=True)
# Source scene is not saved. Hide irrelevant pieces for true Blender diagnostics.
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1500;s.render.resolution_y=1100;s.render.resolution_percentage=100;s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.view_settings.view_transform='Standard'
def shot(name,keys,at,aim,scale):
 for o in geo:o.hide_render=str(o.get('VOY02_ORIGEN','')).removeprefix('OBJ:') not in keys
 cd=bpy.data.cameras.new(name);c=bpy.data.objects.new(name,cd);s.collection.objects.link(c);c.location=Vector(at)+T;c.rotation_euler=(Vector(aim)+T-c.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=scale;cd.clip_start=.005;s.camera=c;s.render.filepath=str(R/'CAPTURAS'/f'{name}.png');bpy.ops.render.render(write_still=True)
for st in stations:
 p=Vector(st['seat_reference_m']);keys=set(st['refined_parts']);near=[]
 for r in rows:
  lo=np.array(r['lo']);hi=np.array(r['hi']);d=np.maximum(np.maximum(lo-np.array(p),np.array(p)-hi),0)
  if np.linalg.norm(d)<1.1 and hi[2]<2.5 and hi[2]>.05:near.append(r['key'])
 shot('A_'+st['id'],keys|set(near),p+Vector((2.8,2.8,2.6)),p+Vector((0,0,.25)),3.8)
 shot('A_'+st['id']+'_AISLADA',keys,p+Vector((1.7,-1.7,1.1)),p+Vector((0,0,.2)),1.8)
print('INSPECCION_TERMINADA',flush=True)
