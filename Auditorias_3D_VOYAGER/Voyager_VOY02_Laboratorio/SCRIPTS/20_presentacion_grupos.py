"""Refine diagnostic chair grouping, repair silhouette neck gaps; no source geometry edits."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];path=R/'ESCENAS/VOY02_Laboratorio.blend'
bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)
assert not bpy.data.scenes['G_INTERIORES_CONECTADOS'].get('VOY02_PRESENTACION_REVISADA'),'Already revised'
fun=json.loads((R/'DATOS/preparacion_funcional.json').read_text());new=json.loads((R/'DATOS/puestos_revision.json').read_text());groups={s['id']:s['refined_parts'] for s in new['stations']};meta={o['name']:o for o in json.loads((R/'DATOS/obj_objetos.json').read_text())};s=bpy.data.scenes['E_SILLAS_GRUPOS'];changes=[]
templates={o.get('VOY02_ORIGEN')[4:]:o for o in bpy.data.scenes['G_INTERIORES_CONECTADOS'].objects if o.type=='MESH' and o.get('VOY02_ORIGEN','').startswith('OBJ:')}
for ch in fun['chairs']:
 name=ch['id'];parts=groups[name];root=bpy.data.objects[name+'_PIVOTE_PRUEBA'];center=ch['pivot_candidate'];bottom=min(meta[n]['bounds_min'][2] for n in ch['parts'])
 for n in set(ch['parts'])-set(parts):
  o=bpy.data.objects.get(name+'_'+n)
  if o:bpy.data.objects.remove(o,do_unlink=True)
 for n in set(parts)-set(ch['parts']):
  o=templates[n].copy();o.data=templates[n].data;o.animation_data_clear();o.name=name+'_'+n;s.collection.objects.link(o);o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Identity(4);o.location=(-center[0],-center[1],-bottom);o['VOY02_ORIGEN']='OBJ:'+n;o['VOY02_TIPO']='GEOMETRIA_EXISTENTE_COPIADA'
 for o in s.objects:
  if o.type=='FONT' and o.name.startswith('LABEL_'+name):o.data.body=name+' / '+str(len(parts))+' PARTES / ARTICULACION NO VALIDADA'
 changes.append(dict(group=name,old=ch['parts'],new=parts))
necks=[]
for scene in bpy.data.scenes:
 for head in list(scene.objects):
  if head.type!='MESH' or not head.name.endswith('_CABEZA'):continue
  torso=bpy.data.objects.get(head.name[:-7]+'_TORSO')
  if not torso:continue
  hp=[head.matrix_world@Vector(p) for p in head.bound_box];tp=[torso.matrix_world@Vector(p) for p in torso.bound_box];lo=max(p.z for p in tp);hi=min(p.z for p in hp)
  if hi<=lo:continue
  cx=sum(p.x for p in hp)/8;cy=sum(p.y for p in hp)/8;verts=[(cx+x*.06,cy+y*.06,z) for x,y,z in [(-1,-1,lo),(1,-1,lo),(1,1,lo),(-1,1,lo),(-1,-1,hi),(1,-1,hi),(1,1,hi),(-1,1,hi)]];faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];me=bpy.data.meshes.new(head.name+'_CUELLO');me.from_pydata(verts,[],faces);me.materials.append(head.data.materials[0]);ob=bpy.data.objects.new(head.name+'_CUELLO',me);scene.collection.objects.link(ob);ob['VOY02_TIPO']='REFERENCIA_HUMANA';necks.append(ob.name)
for scene in bpy.data.scenes:scene['VOY02_PRESENTACION_REVISADA']=True
G=bpy.data.scenes['G_INTERIORES_CONECTADOS']
if bpy.context.window:bpy.context.window.scene=G
# Save useful opening view without hiding the roof or any problem geometry.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_location=(0,4,0);area.spaces.active.region_3d.view_distance=38;area.spaces.active.region_3d.view_rotation=Vector((1,-1,1)).to_track_quat('Z','Y');area.spaces.active.clip_end=10000
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(path))
(R/'DATOS/presentacion_revision.json').write_text(json.dumps(dict(chair_groups=changes,neck_gaps_filled=necks,reference_heights_and_capsules_unchanged=True,scene_count=len(bpy.data.scenes),source_geometry_modified=False,lab_sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2,ensure_ascii=False),encoding='utf8')
print('PRESENTATION',len(changes),'groups',len(necks),'necks',flush=True)
