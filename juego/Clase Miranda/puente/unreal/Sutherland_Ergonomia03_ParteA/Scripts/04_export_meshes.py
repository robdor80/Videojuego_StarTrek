import bpy,bmesh,json,re,traceback,math
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1]
D=R/'Data';out={'ok':False,'visual':[],'doors':[],'collisions':[],'preserved_chairs':[]}
ref=Path(json.loads((D/'copy_verified.json').read_text())['source'])
def safe(s):return re.sub('[^a-zA-Z0-9_]+','_',s).strip('_')
def export(mesh,name,pivot=None):
 obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 dest=R/'Exports'/(name+'.fbx')
 bpy.ops.export_scene.fbx(filepath=str(dest),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_NONE',use_mesh_modifiers=True,mesh_smooth_type='FACE',use_tspace=True,bake_anim=False,path_mode='STRIP')
 bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
 return str(dest)
def old_read():
 bpy.ops.wm.open_mainfile(filepath=str(ref/'Blender/Sutherland_PBR_Recovered.blend'),load_ui=False)
 return {o.name:{'v':np.array([list(o.matrix_world@v.co) for v in o.data.vertices]),'polys':[list(p.vertices) for p in o.data.polygons],'mi':[p.material_index for p in o.data.polygons],'materials':[m.name if m else None for m in o.data.materials]} for o in bpy.context.scene.objects if o.type=='MESH' and len(o.data.vertices)}
try:
 old=old_read();bpy.ops.wm.open_mainfile(filepath=str(R.parents[1]/'blender/Miranda_Puente_Sutherland_Ergonomia_03.blend'),load_ui=False)
 objs={o.name:o for o in bpy.context.scene.objects if o.type=='MESH' and len(o.data.vertices)}
 comp=json.loads((D/'blender_comparison.json').read_text());audit=json.loads((D/'ue_before.json').read_text());assert audit['ok']
 actors={a['label']:a for a in audit['actors']};visualref={x['source']:x for x in json.loads((D/'reference_visual_export.json').read_text())['meshes']}
 doorsources={'Plane.001_0','Plane.017_0','Plane.018_0','Plane.019_0'}
 changed={r['name'] for r in comp['objects'] if r['delta_cm'] is None or r['delta_cm']>.001}
 # Keep all six already assembled, attached chair rigs and their source visuals.
 # Their source originals are not imported a second time.
 for n in sorted(changed):
  if n.startswith('Mesh.') and n not in old:out['preserved_chairs'].append(n);continue
  if n in doorsources:continue
  o=objs[n];world=np.array([list(o.matrix_world@v.co) for v in o.data.vertices]);targets=[n]
  merged=n.startswith('Editable Mesh_Mat.') and n in old and len(world)==2*len(old[n]['v'])
  if merged:
   candidates=[k for k in old if k.startswith(n+'.')];assert len(candidates)==1,(n,candidates)
   targets+=candidates
  for target in targets:
   assert 'VIS_'+target in actors,('No existing actor',target)
   a=old[target];selected=[v.index for v in o.data.vertices if not merged or (world[v.index,0]>0)==(a['v'][:,0].mean()>0)]
   remap={vi:i for i,vi in enumerate(selected)};faces=[p for p in o.data.polygons if all(vi in remap for vi in p.vertices)]
   assert [[remap[v] for v in p.vertices] for p in faces]==a['polys'],('Topology mapping unsafe',n,target)
   mesh=o.data.copy();mesh.transform(o.matrix_world)
   mesh.materials.clear()
   for mn in a['materials']:mesh.materials.append(bpy.data.materials.get(mn) or bpy.data.materials.new(mn))
   for p,mi in zip(faces,a['mi']):mesh.polygons[p.index].material_index=mi
   if merged:
    bm=bmesh.new();bm.from_mesh(mesh);bm.verts.ensure_lookup_table();bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.index not in remap],context='VERTS');bm.to_mesh(mesh);bm.free()
   pv=visualref[target]['pivot_UE_cm'];bp=Vector((pv[0]/100,-pv[1]/100,pv[2]/100));mesh.transform(Matrix.Translation(-bp))
   row={'source':n,'actor_source':target,'asset':actors['VIS_'+target]['components'][0]['mesh'],'file':export(mesh,'ERG_VIS_'+safe(target)),'materials':a['materials'],'expected_world_cm':(world[selected]*np.array([100,-100,100])).tolist()}
   out['visual'].append(row)
 # Export exact source leaves into each retained moving component's local space.
 candidates=[]
 for n in sorted(doorsources):
  o=objs[n];w=np.array([list(o.matrix_world@v.co) for v in o.data.vertices])
  for sign in [-1,1]:
   vi=[i for i in range(len(w)) if w[i,0]*sign>0];pts=w[vi]*np.array([100,-100,100]);candidates.append((n,vi,pts.mean(0)))
 used=set()
 for actor in audit['actors']:
  if 'door' not in actor:continue
  for c in actor['components']:
   idx=min((i for i in range(len(candidates)) if i not in used),key=lambda i:np.linalg.norm(candidates[i][2][:2]-np.array(c['bounds_center'][:2])))
   used.add(idx);n,vi,center=candidates[idx];o=objs[n];mesh=o.data.copy();mesh.transform(o.matrix_world)
   bm=bmesh.new();bm.from_mesh(mesh);bm.verts.ensure_lookup_table();bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.index not in vi],context='VERTS');bm.to_mesh(mesh);bm.free()
   assert abs(c['rotation'][0])+abs(c['rotation'][1])<.001
   yaw=math.radians(c['rotation'][2]);rot=np.array([[math.cos(yaw),-math.sin(yaw),0],[math.sin(yaw),math.cos(yaw),0],[0,0,1]])
   expected=[]
   for v in mesh.vertices:
    ue=np.array(v.co)*np.array([100,-100,100]);expected.append(ue.tolist());local=rot.T@(ue-np.array(c['location']));v.co=Vector(local*np.array([.01,-.01,.01]))
   mesh.materials.clear();mesh.materials.append(bpy.data.materials.get('PBR_Puertas_Burdeos_ConTexto') or bpy.data.materials.new('PBR_Puertas_Burdeos_ConTexto'))
   for p in mesh.polygons:p.material_index=0
   name='ERG_'+actor['door']['door_id']+'_'+c['name'];out['doors'].append({'actor':actor['label'],'component':c['name'],'source':n,'old_asset':c['mesh'],'asset_name':name,'file':export(mesh,name),'expected_world_cm':expected,'materials':c['materials']})
 # Reuse the original collision fabrication face groups. Only affected groups
 # are exported, at their existing pivots; no new general collision system.
 fab=json.loads((ref/'Sources/collision_fabrication.json').read_text())
 for row in fab['exports']:
  if row['name'] not in actors:continue
  parts=row['source_parts']
  if not any(p['object'] in changed for p in parts):continue
  verts=[];faces=[];pivot=row['pivot_UE_cm'];bp=Vector((pivot[0]/100,-pivot[1]/100,pivot[2]/100))
  for part in parts:
   assert part['object'] in objs,('Collision source unavailable',row['name'],part['object'])
   o=objs[part['object']];assert max(part['faces'])<len(o.data.polygons),(row['name'],'face indices')
   for pi in part['faces']:
    p=o.data.polygons[pi];base=len(verts);verts.extend([list(o.matrix_world@o.data.vertices[vi].co-bp) for vi in p.vertices]);faces.append(list(range(base,len(verts))))
  mesh=bpy.data.meshes.new('ERG_COLL');mesh.from_pydata(verts,[],faces);mesh.update()
  out['collisions'].append({'actor':row['name'],'category':row['category'],'asset':actors[row['name']]['components'][0]['mesh'],'file':export(mesh,'ERG_'+row['name']),'source_objects':sorted(set(p['object'] for p in parts))})
 out['ok']=True
except Exception:out['error']=traceback.format_exc();print(out['error'],flush=True)
(D/'export_meshes.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('EXPORT_RESULT',out['ok'],len(out['visual']),len(out['doors']),len(out['collisions']),flush=True)
